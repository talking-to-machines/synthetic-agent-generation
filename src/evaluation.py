import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef
from scipy.stats import chi2_contingency


def evaluate_responses(prompts_with_responses: pd.DataFrame) -> dict:
    """
    Evaluate the LLM's ability to predict the ground truth responses.

    Parameters:
        prompts_with_responses (pd.DataFrame): A DataFrame containing the prompts and the corresponding responses.

    Returns:
        dict: A dictionary containing the evaluation metrics for each question.
    """
    evaluation_results = {}

    for question in prompts_with_responses["question"].unique():
        question_responses = prompts_with_responses[
            prompts_with_responses["question"] == question
        ]

        if (
            question_responses["user_response"].dtype == "int64"
            or question_responses["user_response"].dtype == "float64"
            or pd.to_numeric(question_responses["user_response"], errors="coerce")
            .notnull()
            .all()
        ):
            # Numerical evaluation
            response_type = "Numerical"
            evaluation_result = evaluate_numerical_response(
                question_responses["user_response"], question_responses["llm_response"]
            )

        else:
            # Categorical evaluation
            response_type = "Categorical"
            evaluation_result = evaluate_categorical_response(
                question_responses["user_response"], question_responses["llm_response"]
            )

        evaluation_results[question] = {
            "response_type": response_type,
            "evaluation_result": evaluation_result,
        }

    return evaluation_results


def evaluate_categorical_response(
    user_response: pd.Series, llm_response: pd.Series
) -> dict:
    """
    Evaluate the LLM's ability to predict the user's categorical response in terms of
    cramer's V correlation, accuracy, F1 score, and Matthews correlation coefficient.

    Parameters:
        user_response (pd.Series): A pandas Series containing the user's responses.
        llm_response (pd.Series): A pandas Series containing the LLM's responses.

    Returns:
        dict: A dictionary containing the evaluation metrics.
    """
    # Calculate accuracy
    accuracy = accuracy_score(user_response, llm_response)

    # Calculate F1 score
    f1 = float(f1_score(user_response, llm_response, average="macro"))

    # Calculate Matthews correlation coefficient
    mcc = float(matthews_corrcoef(user_response, llm_response))

    # Calculate Cramer's V correlation
    contingency_table = pd.crosstab(user_response, llm_response)
    chi2, _, _, _ = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()
    epsilon = 1e-10  # Small value to prevent division by zero
    cramer_v = float(
        np.sqrt(chi2 / max((n * (min(contingency_table.shape) - 1)), epsilon))
    )

    return {
        "accuracy": accuracy,
        "macro_f1_score": f1,
        "matthews_corrcoef": mcc,
        "cramer_v": cramer_v,
    }


def evaluate_numerical_response(
    user_response: pd.Series, llm_response: pd.Series
) -> dict:
    """
    Evaluate the LLM's ability to predict the user's numerical response in terms of
    mean absolute error, root mean square error and mean absolute percentage error.

    Parameters:
        user_response (pd.Series): A pandas Series containing the user's responses.
        llm_response (pd.Series): A pandas Series containing the LLM's responses.

    Returns:
        dict: A dictionary containing the evaluation metrics.
    """
    # Convert user_response and llm_response to float type
    user_response = user_response.astype(float)
    llm_response = llm_response.astype(float)

    # Calculate mean absolute error
    mae = float(np.mean(np.abs(user_response - llm_response)))

    # Calculate root mean squared error
    rmse = float(np.sqrt(np.mean((user_response - llm_response) ** 2)))

    # Calculate mean absolute percentage error
    mape = float(np.mean(np.abs((user_response - llm_response) / user_response))) * 100

    return {
        "mean_absolute_error": mae,
        "root_mean_squared_error": rmse,
        "mean_absolute_percentage_error": mape,
    }
