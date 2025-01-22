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


def load_data(filepath: str, drop_first_row: bool = False) -> pd.DataFrame:
    """
    Load the survey data (in either CSV format or Excel format) from a filepath.

    Parameters:
        filepath (str): The path to the survey data file.
        drop_first_row (bool): Whether to drop the first row and use the second row as column headers.

    Returns:
        pd.DataFrame: The survey data.
    """
    if filepath.endswith(".csv"):
        if drop_first_row:
            df = pd.read_csv(filepath, header=1)
        else:
            df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        if drop_first_row:
            df = pd.read_excel(filepath, header=1)
        else:
            df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or XLSX file.")

    return df


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
                "model": "gpt-4o",
                # "model": "gpt-4o-mini",
                # "model": "gpt-4-turbo",
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


def include_variable_names(
    data_with_responses: pd.DataFrame, data_file_path: str
) -> pd.DataFrame:
    """Include variable names from the original data file into the provided DataFrame.
    This function reads the original data file (CSV or XLSX) to extract the column headers,
    maps the current column headers in the provided DataFrame to the original headers,
    and then inserts the current headers as the first row in the resulting DataFrame.

    Args:
        data_with_responses (pd.DataFrame): DataFrame containing the data with responses.
        data_file_path (str): Path to the original data file (CSV or XLSX) containing the headers.
    Returns:
        pd.DataFrame: DataFrame with the original headers included and the current headers as the first row.
    Raises:
        ValueError: If the provided file format is not supported (neither CSV nor XLSX).
    """

    def get_key_by_value(d, value):
        for key, val in d.items():
            if val == value:
                return key
        return value

    if data_file_path.endswith(".csv"):
        original_data_with_headers = pd.read_csv(data_file_path)
    elif data_file_path.endswith(".xlsx"):
        original_data_with_headers = pd.read_excel(data_file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or XLSX file.")

    # Extract the first row from the original data
    col_name_mapping = original_data_with_headers.iloc[0].to_dict()

    new_col_headers = []
    for col in data_with_responses.columns:
        new_col_headers.append(get_key_by_value(col_name_mapping, col))

    # Push the current column headers into the first row
    headers_as_first_row = pd.DataFrame(
        [data_with_responses.columns], columns=data_with_responses.columns
    )

    # Concatenate the headers_as_first_row with the results dataframe
    data_with_response_headers = pd.concat(
        [headers_as_first_row, data_with_responses], ignore_index=True
    )

    # Assign new column headers to the results dataFrame
    data_with_response_headers.columns = new_col_headers

    return data_with_response_headers
