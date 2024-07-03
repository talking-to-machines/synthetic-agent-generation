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
    Generate demographic prompts from the survey data.
    """
    # Generate prompts for demographic information
    # data["demographic_prompt"] = data[demographic_columns].apply(
    #     construct_demographic_prompts, args=(client,), axis=1
    # )

    # Generate prompts for survey questions
    question_prompts = construct_question_prompts(data[survey_questions])

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        for question in survey_questions:
            prompts.append(
                {
                    "custom_id": f"{custom_id_counter}",
                    "user_id": data.loc[i, 'ID'],
                    "survey_context": survey_context,
                    "demographic_info_qna": generate_qna_format(data.loc[i, [demo_question for demo_question in survey_questions if demo_question != question]]),
                    "question_prompt": question_prompts[question],
                    "user_response": data.loc[i, question],
                }
            )
            custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    # Create JSONL batch file
    batch_file_dir = create_batch_file(prompts, question_field='demographic_info_qna', batch_file_name='batch_tasks_demographic_info.jsonl')

    # Get processed demographic information from batch query
    responses = batch_query(client, batch_file_dir)
    responses.rename(columns={'query_response': 'demographic_prompt'}, inplace=True)

    # Merge processed demographic information with prompts
    prompts = merge_prompts_with_responses(prompts, responses)

    # Construct system message using survey context and demographic prompt
    prompts['system_message'] = prompts.apply(lambda row: construct_system_message(row['survey_context'], row['demographic_prompt']), axis=1)

    return prompts

        # demographic_prompt = data.loc[i, "demographic_prompt"]
        # system_message = construct_system_message(survey_context, demographic_prompt)

        # for question in question_columns:
        #     question_prompt = question_prompts[question]
        #     prompts.append(
        #         {
        #             "custom_id": f"{custom_id_counter}",
        #             "system_message": system_message,
        #             "question": question_prompt,
        #             "user_response": data.loc[i, question],
        #         }
        #     )


    # return pd.DataFrame(prompts)


# def construct_demographic_prompts(demographic_info: pd.Series, client: OpenAI) -> str:
#     """
#     Constructs prompts for generating statements describing a subject based on their demographic information.

#     Parameters:
#         demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.
#         client (OpenAI): An instance of the OpenAI client.

#     Returns:
#         str: The generated prompts as a single paragraph.
#     """
#     survey_response = format_survey_response(demographic_info)

#     completion = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "Based on the following survey response from a subject, generate statements describing the subject and start every sentence with 'You'. Write it as a single paragraph and do not mention about the survey.",
#             },
#             {"role": "user", "content": f"{survey_response}"},
#         ],
#     )
#     return completion.choices[0].message.content


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
