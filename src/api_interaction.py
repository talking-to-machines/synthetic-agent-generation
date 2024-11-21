import pandas as pd
import os
import re
from config.settings import HF_TOKEN, HF_HOME

os.environ["HF_HOME"] = HF_HOME
import time
import json
from openai import OpenAI
import ollama
from tqdm import tqdm
from huggingface_hub import InferenceClient
from huggingface_hub import login

login(token=HF_TOKEN)
tqdm.pandas()


def batch_query(
    client: OpenAI, batch_input_file_dir: str, batch_output_file_dir: str
) -> pd.DataFrame:
    """
    Query the LLM using batch processing and return the responses after completion.

    Parameters:
        batch_input_file_dir (str): The directory containing the batch input file.
        batch_output_file_dir (str): The directory containing the batch output file.

    Returns:
        pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    # Upload batch input file
    batch_file = client.files.create(
        file=open(batch_input_file_dir, "rb"), purpose="batch"
    )

    # Create batch job
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )

    # Check batch status
    while True:
        batch_job = client.batches.retrieve(batch_job.id)
        print(f"Batch job status: {batch_job.status}")
        if batch_job.status == "completed":
            break
        elif batch_job.status == "failed":
            raise Exception("Batch job failed.")
        else:
            # Wait for 5 minutes before checking again
            time.sleep(300)

    # Retrieve batch results
    result_file_id = batch_job.output_file_id
    results = client.files.content(result_file_id).content

    # Save the batch output
    current_dir = os.path.dirname(__file__)
    batch_output_dir = os.path.join(
        current_dir, f"../batch_files/{batch_output_file_dir}"
    )
    with open(batch_output_dir, "wb") as file:
        file.write(results)

    # Loading data from saved output file
    response_list = []
    with open(batch_output_dir, "r") as file:
        for line in file:
            # Parsing the JSON result string into a dict
            result = json.loads(line.strip())
            response_list.append(
                {
                    "custom_id": f'{result["custom_id"]}',
                    "query_response": result["response"]["body"]["choices"][0][
                        "message"
                    ]["content"],
                }
            )

    return pd.DataFrame(response_list)


def ollama_query(
    model_name: str,
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str,
) -> pd.DataFrame:
    """
    Query Llama (hosted locally using Ollama) and return the responses after completion.

    Parameters:
        ollama_model (str): The Ollama model name
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.

    Returns:
        pd.DataFrame: The prompts with the corresponding LLM responses.
    """

    def query(row: pd.Series):
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": row[system_message_field]},
                {"role": "user", "content": row[user_message_field]},
            ],
        )
        return response["message"]["content"]

    prompts["llm_response"] = prompts.progress_apply(query, axis=1)

    return prompts


def serverless_query(
    model_name: str,
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str,
) -> pd.DataFrame:
    """
    Query Serverless API and return the responses after completion.

    Parameters:
        model_name (str): The model name
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.

    Returns:
        pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    client = InferenceClient(api_key=HF_TOKEN)

    def query(row: pd.Series):
        if "gemma" in model_name:
            messages = [
                {
                    "role": "user",
                    "content": f"{row[system_message_field]}\n{row[user_message_field]}",
                }
            ]
        else:
            messages = [
                {"role": "system", "content": row[system_message_field]},
                {"role": "user", "content": row[user_message_field]},
            ]
        response = client.chat.completions.create(
            model=model_name, messages=messages, max_tokens=2048, stream=False
        )

        return response.choices[0].message["content"]

    prompts["llm_response"] = prompts.progress_apply(query, axis=1)

    return prompts


def inference_endpoint_query(
    endpoint_url: str,
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str,
    experiment_round: str,
    experiment_version: str,
) -> pd.DataFrame:
    """
    Query dedicated inference endpoint API and return the responses after completion.

    Parameters:
        endpoint_url (str): The endpoint URL
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.

    Returns:
        pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    client = OpenAI(base_url=endpoint_url, api_key=HF_TOKEN)

    current_dir = os.path.dirname(__file__)
    progress_file = os.path.join(
        current_dir, f"../results/{experiment_round}/progress/{experiment_version}.csv"
    )
    # Load progress if exists
    if os.path.exists(progress_file):
        processed_prompts = pd.read_csv(progress_file)
        processed_prompts["ID"] = processed_prompts["ID"].astype("int64")
        prompts = prompts.merge(
            processed_prompts[["ID", "llm_response"]], on="ID", how="left"
        )
    else:
        prompts["llm_response"] = None

    def sanitize_response(response: str) -> str:
        return re.sub(r'[\\/*?:"<>|{}\x00-\x1F\x7F-\x9F]', " ", response)

    def query(row: pd.Series):
        if not pd.isnull(row["llm_response"]):
            return sanitize_response(row["llm_response"])

        # gemma models
        # messages = [{"role": "user", "content": f"{row[system_message_field]}\n{row[user_message_field]}"}]

        # other models
        messages = [
            {"role": "system", "content": row[system_message_field]},
            {"role": "user", "content": row[user_message_field]},
        ]

        response = client.chat.completions.create(
            model="tgi",  # TODO when using dedicated inference endpoint
            # model="meta-llama/Llama-3.1-8B-Instruct",  # TODO When using serverless inference
            messages=messages,
            stream=False,
        )

        row["llm_response"] = response.choices[0].message.content

        # Save progress
        row.to_frame().T.to_csv(
            progress_file,
            mode="a",
            header=not os.path.exists(progress_file),
            index=False,
        )

        return sanitize_response(row["llm_response"])

    prompts["llm_response"] = prompts.progress_apply(query, axis=1)

    return prompts
