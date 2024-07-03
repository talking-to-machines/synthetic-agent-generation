import pandas as pd
from openai import OpenAI
from src.data_processing import (
    merge_prompts_with_responses,
    create_batch_file,
)
from src.api_interaction import batch_query


def generate_prompts(
    client: OpenAI,
    data: pd.DataFrame,
    survey_context: str,
    survey_questions: list,
) -> pd.DataFrame:
    """
    Generate prompts for survey questions.

    Parameters:
        client (OpenAI): The OpenAI client object.
        data (pd.DataFrame): The survey data.
        survey_context (str): The context of the survey.
        survey_questions (list): The list of survey questions.

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    # Generate prompts for survey questions
    question_prompts = construct_question_prompts(data[survey_questions])

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        for question in survey_questions:
            if pd.isnull(data.loc[i, question]):
                continue

            prompts.append(
                {
                    "custom_id": f"{custom_id_counter}",
                    "user_id": data.loc[i, "ID"],
                    "survey_context": survey_context,
                    "system_message_demographic_summarise": "Based on the following survey response from a subject, generate statements describing the subject and start every sentence with 'You'. Write it as a single paragraph and do not mention about the survey.",
                    "demographic_info_qna": generate_qna_format(
                        data.loc[
                            i,
                            [
                                demo_question
                                for demo_question in survey_questions
                                if demo_question != question
                            ],
                        ]
                    ),
                    "question": question,
                    "question_prompt": question_prompts[question],
                    "user_response": data.loc[i, question],
                }
            )
            custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    # Create JSONL batch file
    batch_file_dir = create_batch_file(
        prompts,
        system_message_field="system_message_demographic_summarise",
        user_message_field="demographic_info_qna",
        batch_file_name="batch_input_demographic_info.jsonl",
    )

    # Get processed demographic information from batch query
    processed_demographic_prompts = batch_query(
        client,
        batch_input_file_dir=batch_file_dir,
        batch_output_file_dir="batch_output_demographic_info",
    )
    processed_demographic_prompts.rename(
        columns={"query_response": "demographic_prompt"}, inplace=True
    )

    # Merge processed demographic information with prompts
    prompts = merge_prompts_with_responses(prompts, processed_demographic_prompts)

    # Construct system message using survey context and demographic prompt
    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message(
            row["survey_context"], row["demographic_prompt"]
        ),
        axis=1,
    )

    return prompts


def generate_qna_format(demographic_info: pd.Series) -> str:
    """
    Formats the demographic information of a subject in a Q&A format.

    Parameters:
        demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.

    Returns:
        str: The formatted survey response.
    """
    survey_response = ""
    for question, response in demographic_info.items():
        survey_response += f"Interviewer: {question} Me: {response}\n"

    return survey_response


def construct_question_prompts(questions_df: pd.DataFrame) -> dict:
    """
    Constructs a dictionary of question prompts based on the given DataFrame.

    Parameters:
        questions_df (pd.DataFrame): A DataFrame containing the questions.

    Returns:
        question_prompts (dict): A dictionary where the keys are column names and the values are the corresponding question prompts.
    """
    question_prompts = {}
    for question in questions_df.columns:

        if (
            questions_df[question].dtype == "int64"
            or questions_df[question].dtype == "float64"
            or pd.to_numeric(questions_df[question], errors="coerce").notnull().all()
        ):
            # Numeric responses
            question_prompts[question] = (
                f"{question} Please respond with a numerical number no matter what:"
            )

        else:
            # Cateogrical responses
            possible_responses = questions_df[question].unique()

            if len(possible_responses) > 1:
                question_prompts[question] = (
                    f'{question} Please respond with {", ".join([f"{repr(response)}" for response in possible_responses[:-1]])} or {repr(possible_responses[-1])}:'
                )
            else:
                question_prompts[question] = (
                    f"{question} Please respond with {repr(possible_responses[0])}:"
                )

    return question_prompts


def construct_system_message(survey_context: str, demographic_prompt: str) -> str:
    """
    Constructs system message by combining the survey context and demographic prompt.

    Parameters:
        survey_context (str): The context of the survey.
        demographic_prompt (str): The prompt for demographic information.

    Returns:
        str: The constructed prompt.
    """
    return f"{survey_context} \n\n {demographic_prompt}"
