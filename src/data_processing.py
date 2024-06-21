import pandas as pd
import json
import os


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the survey data (in either CSV format or Excel format) from a filepath.

    Parameters:
    filepath (str): The path to the survey data file.

    Returns:
    pd.DataFrame: The survey data.
    """
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        return pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or XLSX file.")


def clean_data(data: pd.DataFrame, relevant_columns: list) -> pd.DataFrame:
    """
    Clean the survey data of any duplicated records or records with missing values.

    Parameters:
    data (pd.DataFrame): The survey data.
    relevant_columns (list): The list of columns to consider when cleaning the data.

    Returns:
    pd.DataFrame: The cleaned survey data.
    """
    # Remove duplicated records
    data.drop_duplicates(subset=relevant_columns, inplace=True)

    # Remove records with missing values
    data.dropna(subset=relevant_columns, inplace=True)

    return data


def merge_prompts_with_responses(
    prompts: pd.DataFrame, responses: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge prompts with responses based on the 'custom_id' column.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.
        responses (pd.DataFrame): The DataFrame containing LLM responses.

    Returns:
        pd.DataFrame: The merged DataFrame containing prompts with corresponding responses.
    """
    prompts_with_response = pd.merge(left=prompts, right=responses, on="custom_id")

    return prompts_with_response


def create_batch_file(prompts: pd.DataFrame) -> str:
    """
    Create a JSONL batch file from the prompts DataFrame.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.

    Returns:
        str: The path to the created JSONL batch file.
    """
    # Creating an array of json tasks
    tasks = []
    for i in range(len(prompts)):
        task = {
            "custom_id": prompts.loc[i, "custom_id"],
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4-turbo",
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": prompts.loc[i, "system_message"]},
                    {"role": "user", "content": prompts.loc[i, "user_message"]},
                ],
            },
        }
        tasks.append(task)

    # Creating batch file
    current_dir = os.path.dirname(__file__)
    batch_file_name = os.path.join(current_dir, "../batch_files/batch_tasks.jsonl")
    with open(batch_file_name, "w") as file:
        for obj in tasks:
            file.write(json.dumps(obj) + "\n")

    return batch_file_name
