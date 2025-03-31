import pandas as pd
import os
import re
from config.settings import (
    HF_TOKEN,
    HF_HOME,
    ANTROPIC_API_KEY,
    GEMINI_API_KEY,
    TOGETHER_API_KEY,
    GROK_API_KEY,
)

os.environ["HF_HOME"] = HF_HOME
import time
import json
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI
from tqdm import tqdm
from huggingface_hub import login
from together import Together

genai.configure(api_key=GEMINI_API_KEY)
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


def inference_endpoint_query(
    endpoint_url: str,
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str,
    experiment_round: str,
    experiment_version: str,
    model_name: str,
) -> pd.DataFrame:
    """
    Query dedicated inference endpoint API and return the responses after completion for HuggingFace and Deepseek.

    Parameters:
        endpoint_url (str): The endpoint URL
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.
        experiment_round (str): The round of the experiment
        experiment_version (str): The experiment/model version
        model_name (str): The name of the LLM

    Returns:
        pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    current_dir = os.path.dirname(__file__)
    progress_dir = os.path.join(current_dir, f"../results/{experiment_round}/progress")
    progress_file = os.path.join(
        current_dir, f"../results/{experiment_round}/progress/{experiment_version}.csv"
    )

    # Check and create the progress folder if it doesn't exist
    os.makedirs(progress_dir, exist_ok=True)

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

    def hf_query(row: pd.Series):
        if not pd.isnull(row["llm_response"]):
            return sanitize_response(row["llm_response"])

        messages = [
            {"role": "system", "content": row[system_message_field]},
            {"role": "user", "content": row[user_message_field]},
        ]

        response = client.chat.completions.create(
            model="tgi",  # TODO when using dedicated inference endpoint
            # model="mistralai/Mistral-7B-Instruct-v0.3",  # TODO When using serverless inference
            messages=messages,
            # max_tokens=4096,
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

    def grok_query(row: pd.Series):
        if not pd.isnull(row["llm_response"]):
            return sanitize_response(row["llm_response"])

        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[
                {"role": "system", "content": row[system_message_field]},
                {"role": "user", "content": row[user_message_field]},
            ],
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

    def claude_query(row: pd.Series):
        if not pd.isnull(row["llm_response"]):
            return sanitize_response(row["llm_response"])

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=row[system_message_field],
            messages=[
                {"role": "user", "content": row[user_message_field]},
            ],
            stream=False,
        )

        row["llm_response"] = response.content[0].text

        # Save progress
        row.to_frame().T.to_csv(
            progress_file,
            mode="a",
            header=not os.path.exists(progress_file),
            index=False,
        )

        return sanitize_response(row["llm_response"])

    def gemini_query(row: pd.Series):
        if not pd.isnull(row["llm_response"]):
            return sanitize_response(row["llm_response"])

        client = genai.GenerativeModel(
            model_name="gemini-1.5-pro", system_instruction=row[system_message_field]
        )
        response = client.generate_content(row[user_message_field])

        row["llm_response"] = response.text

        # Save progress
        row.to_frame().T.to_csv(
            progress_file,
            mode="a",
            header=not os.path.exists(progress_file),
            index=False,
        )

        return sanitize_response(row["llm_response"])

    if model_name == "huggingface":
        client = OpenAI(base_url=endpoint_url, api_key=HF_TOKEN)
        prompts["llm_response"] = prompts.progress_apply(hf_query, axis=1)

    elif model_name == "together":
        client = Together(api_key=TOGETHER_API_KEY)
        prompts["llm_response"] = prompts.progress_apply(hf_query, axis=1)

    elif model_name == "grok":
        client = OpenAI(base_url="https://api.x.ai/v1", api_key=GROK_API_KEY)
        prompts["llm_response"] = prompts.progress_apply(grok_query, axis=1)

    elif model_name == "claude":
        client = Anthropic(api_key=ANTROPIC_API_KEY)
        prompts["llm_response"] = prompts.progress_apply(claude_query, axis=1)

    elif model_name == "gemini":
        prompts["llm_response"] = prompts.progress_apply(gemini_query, axis=1)

    else:
        raise ValueError(f"Model {model_name} is not supported.")

    return prompts
