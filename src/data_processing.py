import pandas as pd
import json
import os
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


current_dir = os.path.dirname(__file__)
healthcare_accessibility_foot_image = encode_image(
    os.path.join(current_dir, "../data/healthcare_accessibility_foot.png")
)
healthcare_accessibility_motorised_travel_image = encode_image(
    os.path.join(current_dir, "../data/healthcare_accessibility_motorised_travel.png")
)
healthcare_accessibility_travel_time_image = encode_image(
    os.path.join(current_dir, "../data/healthcare_accessibility_travel_time.png")
)
tuberculosis_prevalence_image = encode_image(
    os.path.join(current_dir, "../data/tuberculosis_prevalence.png")
)
neonatal_mortality_rate_image = encode_image(
    os.path.join(current_dir, "../data/neonatal_mortality_rate.png")
)
malaria_prevalence_image = encode_image(
    os.path.join(current_dir, "../data/malaria_prevalence.png")
)


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
    Clean the survey data of any duplicated records.

    Parameters:
        data (pd.DataFrame): The survey data.
        relevant_columns (list): The list of columns to consider when cleaning the data.

    Returns:
        pd.DataFrame: The cleaned survey data.
    """
    # Remove duplicated records
    data.drop_duplicates(subset=relevant_columns, inplace=True)

    return data


def create_batch_file(
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str = "question_prompt",
    batch_file_name: str = "batch_tasks.jsonl",
) -> str:
    """
    Create a JSONL batch file from the prompts DataFrame.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.
        batch_file_name (str): The name of the batch file.

    Returns:
        str: The path to the created JSONL batch file.
    """
    # Creating an array of json tasks
    tasks = []
    for i in range(len(prompts)):
        task = {
            "custom_id": f'{prompts.loc[i, "custom_id"]}',
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                # "model": "gpt-4o",
                # "model": "gpt-4o-mini",
                "model": "gpt-4-turbo",
                "temperature": 0,
                "messages": [
                    {"role": "system", "content": prompts.loc[i, system_message_field]},
                    {"role": "user", "content": prompts.loc[i, user_message_field]},
                ],
            },
        }
        tasks.append(task)

    # Creating batch file
    current_dir = os.path.dirname(__file__)
    batch_file_name = os.path.join(current_dir, f"../batch_files/{batch_file_name}")
    with open(batch_file_name, "w") as file:
        for obj in tasks:
            file.write(json.dumps(obj) + "\n")

    return batch_file_name


def create_batch_file_with_image(
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str = "question_prompt",
    batch_file_name: str = "batch_tasks.jsonl",
) -> str:
    """
    Create a JSONL batch file from the prompts DataFrame.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.
        batch_file_name (str): The name of the batch file.

    Returns:
        str: The path to the created JSONL batch file.
    """
    # Creating an array of json tasks
    tasks = []
    for i in range(len(prompts)):
        task = {
            "custom_id": f'{prompts.loc[i, "custom_id"]}',
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4-turbo",
                "temperature": 0,
                "messages": [
                    {"role": "system", "content": prompts.loc[i, system_message_field]},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Map 1 (below) depicts the Upper West Region of Ghana, highlighting the population's accessibility to primary healthcare facilities by foot within the World Health Organization's recommended 5 km distance.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{healthcare_accessibility_foot_image}"
                                },
                            },
                            {
                                "type": "text",
                                "text": "Map 2 (below) depicts the Upper West Region of Ghana, highlighting the population's level of healthcare accessibility based on travel time when driving to district hospitals, measured in minutes.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{healthcare_accessibility_travel_time_image}"
                                },
                            },
                            {
                                "type": "text",
                                "text": "Map 3 (below) depicts the map of Ghana, highlighting the prevalence of Tuberculosis cases in different regions of Ghana in 2018.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{tuberculosis_prevalence_image}"
                                },
                            },
                            {
                                "type": "text",
                                "text": "Map 4 (below) depicts the map of Ghana, highlighting the crude incidence of Malaria cases (per 1000 people) in different regions of Ghana in 2021-2022.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{malaria_prevalence_image}"
                                },
                            },
                            {
                                "type": "text",
                                "text": prompts.loc[i, user_message_field],
                            },
                        ],
                    },
                ],
            },
        }
        tasks.append(task)

    # Creating batch file
    current_dir = os.path.dirname(__file__)
    batch_file_name = os.path.join(current_dir, f"../batch_files/{batch_file_name}")
    with open(batch_file_name, "w") as file:
        for obj in tasks:
            file.write(json.dumps(obj) + "\n")

    return batch_file_name


def create_finetune_batch_file(
    prompts: pd.DataFrame,
    system_message_field: str,
    user_message_field: str = "question_prompt",
    user_response_field: str = "response",
    batch_file_name: str = "batch_tasks.jsonl",
) -> str:
    """
    Create a JSONL batch file from the prompts DataFrame for batch fine-tuning.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.
        system_message_field (str): The column name indicating the system message.
        user_message_field (str): The column name indicating the user message.
        user_response_field (str): The column name indicating the ground truth user response.
        batch_file_name (str): The name of the batch file.

    Returns:
        str: The path to the created JSONL batch file.
    """
    # Creating an array of json tasks
    tasks = []
    for i in range(len(prompts)):
        task = {
            "messages": [
                {"role": "system", "content": prompts.loc[i, system_message_field]},
                {"role": "user", "content": prompts.loc[i, user_message_field]},
                {"role": "assistant", "content": prompts.loc[i, user_response_field]},
            ]
        }
        tasks.append(task)

    # Creating batch file
    current_dir = os.path.dirname(__file__)
    batch_file_name = os.path.join(current_dir, f"../batch_files/{batch_file_name}")
    with open(batch_file_name, "w") as file:
        for obj in tasks:
            file.write(json.dumps(obj) + "\n")

    return batch_file_name
