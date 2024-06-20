import pandas as pd
import numpy as np


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
    Merge prompts with responses based on the 'task_index' column.

    Parameters:
        prompts (pd.DataFrame): The DataFrame containing prompts.
        responses (pd.DataFrame): The DataFrame containing LLM responses.

    Returns:
        pd.DataFrame: The merged DataFrame containing prompts with corresponding responses.
    """
    prompts_with_response = pd.merge(left=prompts, right=responses, on="task_index")

    return prompts_with_response
