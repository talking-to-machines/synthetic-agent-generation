import pandas as pd
import numpy as np
import nltk
from sklearn.metrics import accuracy_score
from src.data_processing import is_categorical
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef
from scipy.stats import chi2_contingency
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer


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

        elif is_categorical(question_responses["user_response"]):
            # Categorical evaluation
            response_type = "Categorical"
            evaluation_result = evaluate_categorical_response(
                question_responses["user_response"], question_responses["llm_response"]
            )

        else:
            # Free text evaluation
            response_type = "Free Text"
            evaluation_result = evaluate_free_text_response(
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
    f1 = f1_score(user_response, llm_response, average="macro")

    # Calculate Matthews correlation coefficient
    mcc = matthews_corrcoef(user_response, llm_response)

    # Calculate Cramer's V correlation
    contingency_table = pd.crosstab(user_response, llm_response)
    chi2, _, _, _ = chi2_contingency(contingency_table)
    n = contingency_table.sum().sum()
    cramer_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))

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
    mae = np.mean(np.abs(user_response - llm_response)).item()

    # Calculate root mean squared error
    rmse = np.sqrt(np.mean((user_response - llm_response) ** 2)).item()

    # Calculate mean absolute percentage error
    mape = np.mean(np.abs((user_response - llm_response) / user_response)).item() * 100

    return {
        "mean_absolute_error": mae,
        "root_mean_squared_error": rmse,
        "mean_absolute_percentage_error": mape,
    }


def evaluate_free_text_response(
    user_response: pd.Series, llm_response: pd.Series
) -> dict:
    """
    Evaluate the LLM's ability to predict the user's free text response in terms of
    BLEU score and ROUGE score.

    Parameters:
        user_response (pd.Series): A pandas Series containing the user's responses.
        llm_response (pd.Series): A pandas Series containing the LLM's responses.

    Returns:
        dict: A dictionary containing the evaluation metrics.
    """
    nltk.download("punkt")

    # Initialize ROUGE scorer
    rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

    # Initialize BLEU components
    smoothing_function = SmoothingFunction().method1

    # Containers for scores
    bleu_scores = []
    rouge1_scores = []
    rouge2_scores = []
    rougeL_scores = []

    for ref_text, cand_text in zip(user_response, llm_response):
        # Tokenize texts for BLEU
        ref_tokens = nltk.word_tokenize(ref_text.lower())
        cand_tokens = nltk.word_tokenize(cand_text.lower())

        # Calculate BLEU score
        bleu_score = sentence_bleu(
            [ref_tokens], cand_tokens, smoothing_function=smoothing_function
        )
        bleu_scores.append(bleu_score)

        # Calculate ROUGE scores
        rouge_scores = rouge.score(ref_text, cand_text)
        rouge1_scores.append(rouge_scores["rouge1"].fmeasure)
        rouge2_scores.append(rouge_scores["rouge2"].fmeasure)
        rougeL_scores.append(rouge_scores["rougeL"].fmeasure)

    # Calculate averages
    avg_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
    avg_rouge1 = sum(rouge1_scores) / len(rouge1_scores) if rouge1_scores else 0
    avg_rouge2 = sum(rouge2_scores) / len(rouge2_scores) if rouge2_scores else 0
    avg_rougeL = sum(rougeL_scores) / len(rougeL_scores) if rougeL_scores else 0

    return {
        "average_bleu": avg_bleu,
        "average_rouge1": avg_rouge1,
        "average_rouge2": avg_rouge2,
        "average_rougeL": avg_rougeL,
    }
