import pandas as pd
from openai import OpenAI
from src.data_processing import (
    merge_prompts_with_responses,
    create_batch_file,
)
from src.api_interaction import batch_query

question_options = {
    "Over the past year, how often, if ever, have you or anyone in your family gone without Medicines or medical treatment?": [
        "Just once or twice",
        "Several times",
        "Never",
        "Many times",
        "Always",
    ],
    "In the past 12 months, have you had contact with a public clinic or hospital?": [
        "Yes",
        "No",
    ],
    "How easy or difficult was it to obtain the medical care or services you needed?": [
        "Very easy",
        "Easy",
        "Very Difficult",
        "Difficult",
    ],
    "Please tell me whether you personally or any other member of your household have became ill with, or tested positive for COVID-19 by the COVID-19 pandemic?": [
        "No",
        "Yes",
    ],
    "Please tell me whether you personally or any other member of your household have temporarily or permanently lost a job, business, or primary source of income by the COVID-19 pandemic?": [
        "No",
        "Yes",
    ],
    "Have you received a vaccination against COVID-19, either one or two doses?": [
        "No",
        "Yes",
    ],
    "If a vaccine for COVID-19 is available , how likely are you to try to get vaccinated?": [
        "Somewhat unlikely",
        "Very unlikely",
        "Very likely",
        "Somewhat likely",
        "Don't know",
    ],
    "What is the main reason that you would be unlikely to get a COVID-19 vaccine?": [
        "Vaccine is not safe",
        "COVID doesn't exist / COVID is not real",
        "Some other reason",
        "Don't trust the vaccine/worried about getting fake or counterfeit vaccine",
        "Don't like needles",
        "God will protect me",
        "Afraid of vaccines in general",
        "Vaccine may cause infertility",
        "I am at no risk or low risk for getting COVID / Small chance of contracting COVID",
        "Not worried about COVID / COVID is not serious or life-threatening/not deadly",
        "I already had COVID and believe I am immune",
        "Vaccine was developed too quickly",
        "Vaccine may cause other bad side effects",
        "Don't know",
        "Allergic to vaccines",
        "Religious objections to vaccines in general or to the COVID vaccine",
        "Vaccine is not effective / Vaccinated people can still get COVID",
        "I don't know how to get the vaccine",
        "Vaccines are being used to control or track people",
        "Effective treatments for COVID are or will be available",
        "I will get the vaccine later",
        "Don't trust the vaccine source / Will wait for other vaccines",
        "People are being experimented on with vaccines",
        "I will wait until others have been vaccinated",
        "Vaccine may cause COVID",
        "Vaccine will be too expensive",
        "Refused to answer",
        "It is too difficult to get the vaccine, e.g. have to travel far",
    ],
    "How much do you trust the government to ensure that any vaccine for COVID-19 that is developed or offered to Nigerian citizens is safe before it is used in this country?": [
        "Just a little",
        "Not at all",
        "Somewhat",
        "A lot",
        "Don't know",
        "Refused",
    ],
}


def generate_prompts(
    client: OpenAI,
    data: pd.DataFrame,
    survey_context: str,
    demographic_questions: list,
    survey_questions: list,
) -> pd.DataFrame:
    """
    Generate prompts for survey questions.

    Parameters:
        client (OpenAI): The OpenAI client object.
        data (pd.DataFrame): The survey data.
        survey_context (str): The context of the survey.
        demographic_questions (list): The list of demographic questions.
        survey_questions (list): The list of survey questions.

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    # Generate prompts for asking survey questions
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
                        data.loc[i, demographic_questions],
                    ),
                    # "demographic_info_qna": generate_qna_format_2ndperson(
                    #     data.loc[i, demographic_questions],
                    # ),
                    "question": question,
                    "question_prompt": question_prompts[question],
                    "user_response": data.loc[i, question],
                }
            )
            custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    ###### Demographic Information in 'You' Statements (Start) ######
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
    ###### Demographic Information in 'You' Statements (End) ######

    ###### Demographic Information in Q&A Format (Start) ######
    # prompts["system_message"] = prompts.apply(
    #     lambda row: construct_system_message(
    #         row["survey_context"], row["demographic_info_qna"]
    #     ),
    #     axis=1,
    # )
    ###### Demographic Information in Q&A Format (End) ######

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
        survey_response += f"Interviewer: {question} Me: {response} "

    return survey_response


def generate_qna_format_2ndperson(demographic_info: pd.Series) -> str:
    """
    Formats the demographic information of a subject in 2nd person.

    Parameters:
        demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.

    Returns:
        str: The formatted survey response.
    """
    case_code = {
        "Do you come from a rural or urban area?": lambda: f"You come from a {response} area.",
        "How old are you?": lambda: f"You are {response} years old.",
        "What is your gender?": lambda: f"You are a {response}.",
        "What is your race?": lambda: f"You are {response}.",
        "What is the primary language you speak in your home?": lambda: f"The primary language you speak in your home is {response}.",
        "What is your highest level of education?": lambda: f"Your highest level of education is {response}.",
        "What is your religion, if any?": lambda: f"Your religion is {response}.",
        "What is your ethnic community or cultural group?": lambda: f"Your ethnic community or cultural group is {response}.",
        "Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job?": lambda: f"On whether you have a job that pays a cash income, your response is {response}.",
        "What is your main occupation? If unemployed, retired, or disabled, what was your last main occupation?": lambda: f"Your main/previous occupation is {response}.",
        "Do you personally own a mobile phone? If not, does anyone else in your household own one?": lambda: f"On whether you or someone else in your household personally owns a mobile phone, your response is {response}.",
        "In general, how would you describe your own present living conditions?": lambda: f"In general, you would describe your present living conditions as {response}.",
        "What region do you come from?": lambda: f"You come from the {response} region.",
        "Does the enumeration area have an electricity grid that most houses can access?": lambda: f"On whether you live in an area that has an electricity grid that most houses can access, your response is {response}.",
        "Does the enumeration area have a piped water system that most houses can access?": lambda: f"On whether you live in an area that has a piped water system that most houses can access, your response is {response}.",
        "Does the enumeration area have a sewage system that most houses can access?": lambda: f"On whether you live in an area that has a sewage system that most houses can access, your response is {response}.",
        "Does the enumeration area have a mobile phone service that most houses can access?": lambda: f"On whether you live in an area that has a mobile phone service that most houses can access, your response is {response}.",
        "Are health clinics (private or public or both) present in the enumeration area or in easy walking distance?": lambda: f"On whether you live in an area that has private or public healthcare clinics within easy walking distance, your response is {response}.",
        "What is your main source of water for household use?": lambda: f"Your main source of water for household use is {response}.",
        "Do you have an electric connection to your home from the Electricity Company of Ghana, ECG, or the Northern Electricty Distribution Company Ltd, NEDCO?": lambda: f"On whether you have an electricity connection to your home, your response is {response}.",
        "Do you personally own a mobile phone? If yes, does your phone have access to the Internet?": lambda: f"On whether you personally own a mobile phone that has access to Internet, your response is {response}.",
        "Do you feel close to any particular political party?": lambda: f"On whether you feel close to a particular political party, your response is {response}.",
        "In general, how would you describe the present economic condition of this country?": lambda: f"You would describe the present economic condition of this country as {response}.",
        "When you get together with your friends or family, how often would you say you discuss political matters?": lambda: f"When you get together with your friends or family, you {response} discuss political matters.",
        "In this country, how free are you to say what you think?": lambda: f"In this country, you are {response} to say what you think.",
        "Over the past year, how often, if ever, have you or anyone in your family felt unsafe walking in your neighborhood?": lambda: f"Over the past year, you have {response} felt unsafe walking in your neighborhood.",
        "Over the past year, how often, if ever, have you or anyone in your family feared crime in your own home?": lambda: f"Over the past year, you or anyone in your family have {response} feared crime in your own home.",
        "In this country, how free are you to join any political organization you want?": lambda: f"In this country, you feel {response} to join any political organization you want.",
        "In this country, how free are you to choose who to vote for without feeling pressured?": lambda: f"In this country, you feel {response} to choose who to vote for without feeling pressured.",
        "During the past year, how often have you contacted an assemby man or woman about some important problem or to give them your views?": lambda: f"During the past year, you have {response} contacted an assembly man or woman about some important problem or to give them your views.",
        "During the past year, how often have you contacted a member of Parliament about some important problem or to give them your views?": lambda: f"During the past year, you have {response} contacted a member of Parliament about some important problem or to give them your views.",
        "During the past year, how often have you contacted a political party official about some important problem or to give them your views?": lambda: f"During the past year, you have {response} contacted a political party official about some important problem or to give them your views.",
        "During the past year, how often have you contacted a traditional leader about some important problem or to give them your views?": lambda: f"During the past year, you have {response} contacted a traditional leader about some important problem or to give them your views.",
        "Overall, how satisfied are you with the way democracy works in Ghana?": lambda: f"Overall, your view on the way democracy works in Ghana is {response}.",
        "In your opinion, how often, in this country do people have to be careful of what they say about politics?": lambda: f"In your opinion, people in your country {response} have to be careful of what they say about politics.",
        "In your opinion, how often, in this country are people treated unequally under the law?": lambda: f"In your opinion, people in this country are {response} treated unequally under the law.",
        "How often, if ever, are people treated unfairly by the government based on their economic status, that is, how rich or poor they are?": lambda: f"If people in this country are {response} treated unfairly by the government based on their economic status.",
        "To whom do you normally go to first for assistance, when you are concerned about your security and the security of your family?": lambda: f"When you are concerned about your security and the security of your family, you normally go to {response}.",
        "How much do you trust other Ghanaians?": lambda: f"You trust other Ghanaians {response}.",
        "How much do you trust your relatives?": lambda: f"You trust your relatives {response}.",
        "How much do you trust your neighbours?": lambda: f"You trust your neighbours {response}.",
        "How much do you trust other people you know?": lambda: f"You trust other people you know {response}.",
        "How much do you trust people from other religions?": lambda: f"You trust people from other religions {response}.",
        "How much do you trust people from other ethnic groups?": lambda: f"You trust people from other ethnic groups {response}.",
        "How often do you use the Internet?": lambda: f"You use the Internet {response}.",
        "In your opinion, what are the most important problems facing this country that government should address?": lambda: f"In your opinion, the most important problems facing this country that the government should address are {response}.",
        "In general, when dealing with health workers and clinic or hospital staff, how much do you feel that they treat you with respect?": lambda: f"In general, when dealing with health workers and clinic or hospital staff, you feel that they treat you with respect {response}.",
        "And have you encountered long waiting time with a public clinic or hospital during the past 12 months?": lambda: f"On whether you have encountered long waiting time with a public clinic or hospital during the past 12 months, your response is {response}.",
    }

    survey_response = ""
    for question, response in demographic_info.items():
        if (
            pd.isnull(response)
            or "don't know" in str(response).lower()
            or "refused to answer" in str(response).lower()
        ):
            continue
        # Execute the code for the corresponding case
        survey_response += f"{case_code.get(question, '')(response)} "

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
                f"{question} Please only respond with a numerical value and do not return a text response:"
            )

        else:
            # Cateogrical responses
            options = question_options[question]
            question_prompts[question] = (
                f'{question} Please respond with {", ".join([f"{repr(option)}" for option in options[:-1]])} or {repr(options[-1])}:'
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
    return f"{survey_context}\n\n{demographic_prompt}"
