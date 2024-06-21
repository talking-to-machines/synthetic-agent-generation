import pandas as pd
import os
import time
from openai import OpenAI


def query_llm(client: OpenAI, batch_file_dir: str) -> pd.DataFrame:
    """
    Query the LLM using batch processing and return the responses after completion.

    Parameters:
    batch_file_dir (str): The directory containing the batch input file.

    Returns:
    pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    # Upload batch input file
    batch_file = client.files.create(file=open(batch_file_dir, "rb"), purpose="batch")

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
        else:
            # Wait for 10 minutes before checking again
            time.sleep(600)

    # Retrieve batch results
    result_file_id = batch_job.output_file_id
    results = client.files.content(result_file_id).content

    response_list = []
    for result in results:
        response_list.append(
            {
                "custom_id": result["custom_id"],
                "response": result["response"]["body"]["choices"][0]["message"][
                    "content"
                ],
            }
        )

    return pd.DataFrame(response_list)
