import pandas as pd
from openai import OpenAI
from src.data_processing import is_categorical


def generate_prompts(
    client: OpenAI,
    data: pd.DataFrame,
    survey_context: str,
    demographic_columns: list,
    question_columns: list,
) -> pd.DataFrame:
    """
    Generate prompts from the survey data.
    """
    # Generate prompts for demographic information
    data['demographic_prompt'] = data[demographic_columns].apply(construct_demographic_prompts, args=(client,), axis=1)

    # Generate prompts for survey questions
    question_prompts = construct_question_prompts(data[question_columns])

    # Iterate through the data and generate prompts
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        demographic_prompt = data.loc[i, 'demographic_prompt']
        system_message = construct_system_message(survey_context, demographic_prompt)

        for question in question_columns:
            question_prompt = question_prompts[question]
            prompts.append({
                "custom_id": custom_id_counter,
                "system_message": system_message,
                "question": question_prompt,
                "user_response": data.loc[i, question]
            })

            custom_id_counter += 1
    return pd.DataFrame(prompts)


def construct_demographic_prompts(demographic_info: pd.Series, client: OpenAI) -> str:
    """
    Constructs prompts for generating statements describing a subject based on their demographic information.

    Parameters:
        demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.
        client (OpenAI): An instance of the OpenAI client.

    Returns:
        str: The generated prompts as a single paragraph.
    """
    survey_response = format_survey_response(demographic_info)

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Based on the following survey response from a subject, generate statements describing the subject and start every sentence with 'You'. Write it as a single paragraph and do not mention about the survey."},
            {"role": "user", "content": f"{survey_response}"}
        ]
    )
    return completion.choices[0].message


def format_survey_response(demographic_info: pd.Series) -> str:
    """
    Formats the demographic information of a subject as a survey response.

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

        if questions_df[question].dtype == 'int64' or questions_df[question].dtype == 'float64':
            # Numeric responses
            question_prompts[question] = f'{question} Please respond with a numerical number:'

        elif is_categorical(questions_df[question]):
            # Cateogrical responses
            possible_responses = questions_df[question].unique()

            if len(possible_responses) > 1:    
                question_prompts[question] = f'{question} Please respond with {", ".join([f"{repr(response)}" for response in possible_responses[:-1]])} or {repr(possible_responses[-1])}:'
            else:
                question_prompts[question] = f'{question} Please respond with {repr(possible_responses[0])}:'

        else:  
            # Free text responses
            question_prompts[question] = f'{question} Please respond as free text in a concise manner:'

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
    return f"
    {survey_context} \n\n
    {demographic_prompt}
    "