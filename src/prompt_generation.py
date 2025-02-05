import pandas as pd
from typing import Any

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
        "Likely",
        "Unlikely",
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
    "Have you received a COVID-19 vaccine?": ["No", "Yes"],
}

treatment_video_transcript = {
    # Vaccination Intent
    # "CDC Health": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID 19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. Getting the COVID-19 vaccine will help prevent you from getting COVID-19 and reduce your risk of being hospitalized with COVID-19. COVID 19 vaccine help you to protect yourself your environment and your loved ones from COVID-19 exposure.",
    # "Placebo": "The Sun lights up our lives for business for education even for socializing but when the Sun sets many people use candles who are quality battery-operated torches and kerosene lamps as inefficient and expensive ways to create light. What if you can take some Sun with you at night?  You can with portable solar products there are different types, but each portable solar product is made up of three basic parts: a small solar panel, a modern rechargeable battery and an LED bulb. The solar panel catches the light from the Sun and stores this energy in the battery. This can now be used for much needed light when it's dark. Many can even charge phones portable solar products should be reliable affordable and warranted be sure to demand top quality solar products look for these products lighting Africa shining the way.",
    # "Low Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 20 Cedi. If you get vaccinated, you will get rewarded.",
    # "High Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 60 Cedi. If you get vaccinated, you will get rewarded.",
    # Vaccination Outcome
    "CDC Health": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID 19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. Getting the COVID-19 vaccine will help prevent you from getting COVID-19 and reduce your risk of being hospitalized with COVID-19. COVID 19 vaccine help you to protect yourself your environment and your loved ones from COVID-19 exposure.\n\nWe indicated that we will follow up with you in 6 weeks. We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification",
    "Placebo": "The Sun lights up our lives for business for education even for socializing but when the Sun sets many people use candles who are quality battery-operated torches and kerosene lamps as inefficient and expensive ways to create light. What if you can take some Sun with you at night?  You can with portable solar products there are different types, but each portable solar product is made up of three basic parts: a small solar panel, a modern rechargeable battery and an LED bulb. The solar panel catches the light from the Sun and stores this energy in the battery. This can now be used for much needed light when it's dark. Many can even charge phones portable solar products should be reliable affordable and warranted be sure to demand top quality solar products look for these products lighting Africa shining the way.\n\nWe indicated that we will follow up with you in 6 weeks. We will contact you in order to verify your vaccination status.  If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification.",
    "Low Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 20 Cedi. If you get vaccinated, you will get rewarded.\n\nWe indicated that we will follow up with you in 30 days.  We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification and you will be paid your 20 Cedi via cell phone money payment or by cash if you prefer.",
    "High Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 60 Cedi. If you get vaccinated, you will get rewarded.\n\nWe indicated that we will follow up with you in 6 weeks.  We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification and you will be paid your 60 Cedi via cell phone money payment or by cash if you prefer.",
    # "TBHealth": "Health authorities are working hard to test people for being at risk of getting ill with Tuberculosis. If you are at risk you will be treated to stop you getting ill with Tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from Tuberculosis. One in four people have sleeping Tuberculosis. If you have sleeping Tuberculosis, you will feel well, but there is a risk that the Tuberculosis bacteria will wake up and give you active Tuberculosis, a serious illness. Getting tested and treated for sleeping Tuberculosis will prevent you from getting active Tuberculosis and reduce your risk of being hospitalized with Tuberculosis. Tuberculosis testing will help you to protect yourself your environment and your loved ones from Tuberculosis exposure. We have two further questions to ask and then the survey will end.",
    # "TBHealthPlus3": "Health authorities are working hard to test people for being at risk of getting ill with Tuberculosis. If you are at risk you will be treated to stop you getting ill with Tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from Tuberculosis. If you show up for the scheduled Tuberculosis testing in your village and get the Tuberculosis test you will receive 20 Cedi. If you get Tuberculosis tested, you will get rewarded. We have two further questions to ask and then the survey will end.",
    # "TBHealthPlusText": "Health authorities are working hard to test people for being at risk of getting ill with Tuberculosis. If you are at risk you will be treated to stop you getting ill with Tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from Tuberculosis. One in four people have sleeping Tuberculosis. If you have sleeping Tuberculosis, you will feel well, but there is a risk that the Tuberculosis bacteria will wake up and give you active Tuberculosis, a serious illness. Getting tested and treated for sleeping Tuberculosis will prevent you from getting active Tuberculosis and reduce your risk of being hospitalized with Tuberculosis. Tuberculosis testing will help you to protect yourself your environment and your loved ones from Tuberculosis exposure. You also received a text message reminding you to go for your Tuberculosis screening appointment. We have two further questions to ask and then the survey will end.",
}


def generate_candor_prompts(
    data: pd.DataFrame,
    demographic_questions: list,
    survey_questions: list,
    include_backstory: bool,
    backstory_file_path: str = "",
    supplementary_file_path: str = "",
) -> pd.DataFrame:
    """
    Generate prompts for survey questions.

    Parameters:
        data (pd.DataFrame): The survey data.
        demographic_questions (list): The list of demographic questions.
        survey_questions (list): The list of survey questions.
        include_backstory (bool): Indicates if the subject's backstory should be included.
        backstory_file_path (str): Indicates the file path to the backstory file
        supplementary_file_path (str): Indicates the file path to the supplementary country file

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    demographic_questions.remove("country")

    if include_backstory:
        # Load backstories
        backstories = pd.read_excel(backstory_file_path)
        data = pd.merge(left=data, right=backstories[["ID", "backstory"]], on="ID")

    # Load country supplementary data
    supplementary_data = pd.read_excel(supplementary_file_path)
    data = pd.merge(left=data, right=supplementary_data, on="country")

    # Generate prompts for asking survey questions
    question_prompts = construct_question_prompts(data[survey_questions])

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        # Extract subject backstory
        if include_backstory:
            backstory = f"\n\n{data.loc[i, 'backstory']}"
        else:
            backstory = ""

        for question in survey_questions:
            if pd.isnull(data.loc[i, question]):
                continue

            prompts.append(
                {
                    "custom_id": f"{custom_id_counter}",
                    "ID": data.loc[i, "ID"],
                    "survey_context": data.loc[i, "replication_instruction_prompt"]
                    + data.loc[i, "replication_fewshot_demographic"],
                    "demographic_info": generate_qna_format(
                        data.loc[i, demographic_questions],
                    )
                    + backstory,
                    "question": question,
                    "question_prompt": question_prompts[question],
                    "user_response": data.loc[i, question],
                }
            )
            custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message(
            row["survey_context"], row["demographic_info"]
        ),
        axis=1,
    )

    return prompts


def generate_backstory_prompts(
    data: pd.DataFrame,
    demographic_questions: list,
) -> pd.DataFrame:
    """
    Generate prompts for creating backstories.

    Parameters:
        data (pd.DataFrame): The survey data.
        demographic_questions (list): The list of demographic questions.

    Returns:
        pd.DataFrame: The prompts generated for creating backstories for each user.
    """
    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):

        ### Configuration for Backstory (START) ###
        # demographic_info = generate_qna_format(data.loc[i, demographic_questions])
        # prompts.append(
        #     {
        #         "custom_id": f"{custom_id_counter}",
        #         "ID": data.loc[i, "ID"],
        #         "demographic_info": demographic_info,
        #         "system_message": f"You are asked to complete some interview questions below\n\n{demographic_info}",
        #         "question_prompt": "Create your backstory based on the information provided. Please describe in detail in first person narration.",
        #     }
        # )
        ### Configuration for Backstory (END) ###

        ### Configuration for Interview Summary (START) ###
        # demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        # prompts.append(
        #     {
        #         "custom_id": f"{custom_id_counter}",
        #         "ID": data.loc[i, "ID"],
        #         "demographic_info": demographic_info,
        #         "system_message": f"Here is a conversation between an interviewer and an interviewee\n\n{demographic_info}",
        #         "question_prompt": "Succinctly summarize the facts about the interviewee based on the conversation above in a few bullet points in first person narration -- again, think short, concise bullet points",
        #     }
        # )
        ### Configuration for Interview Summary (END) ###

        ### Configuration for Expert Reflection Psychologist (START) ###
        # demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        # prompts.append(
        #     {
        #         "custom_id": f"{custom_id_counter}",
        #         "ID": data.loc[i, "ID"],
        #         "demographic_info": demographic_info,
        #         "system_message": f"Imagine you are an expert psychologist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
        #         "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
        #     }
        # )
        ### Configuration for Expert Reflection Psychologist (END) ###

        ### Configuration for Expert Reflection Economist (START) ###
        # demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        # prompts.append(
        #     {
        #         "custom_id": f"{custom_id_counter}",
        #         "ID": data.loc[i, "ID"],
        #         "demographic_info": demographic_info,
        #         "system_message": f"Imagine you are an expert economist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
        #         "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
        #     }
        # )
        ### Configuration for Expert Reflection Economist (END) ###

        ### Configuration for Expert Reflection Political Scientist (START) ###
        # demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        # prompts.append(
        #     {
        #         "custom_id": f"{custom_id_counter}",
        #         "ID": data.loc[i, "ID"],
        #         "demographic_info": demographic_info,
        #         "system_message": f"Imagine you are an expert political scientist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
        #         "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
        #     }
        # )
        ### Configuration for Expert Reflection Political Scientist (END) ###

        ### Configuration for Expert Reflection Demographer (START) ###
        demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "demographic_info": demographic_info,
                "system_message": f"Imagine you are an expert demographer (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
                "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
            }
        )
        ### Configuration for Expert Reflection Demographer (END) ###

        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    return prompts


def generate_replication_experiment_prompts(
    data: pd.DataFrame,
    survey_context: str,
    demographic_questions: list,
    question: str,
    include_backstory: bool,
    backstory_file_path: str = "",
) -> pd.DataFrame:
    """
    Generate prompts for synthetic experiment.

    Parameters:
        data (pd.DataFrame): The survey data.
        survey_context (str): The context of the survey.
        demographic_questions (list): The list of demographic questions.
        question (str): The question to be answered.
        include_backstory (bool): Indicates if the subject's backstory should be included.
        backstory_file_path (str): Indicates the file path to the backstory file

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    if include_backstory:
        # Load backstories
        backstories = pd.read_excel(backstory_file_path)
        # backstories.rename(columns={"expert_reflection_combined":"backstory"}, inplace=True)
        data = pd.merge(left=data, right=backstories[["ID", "backstory"]], on="ID")

    ### Configuration for Interview Summary (START) ###
    # import os
    # current_dir = os.path.dirname(__file__)
    # interview_summary_file_path = os.path.join(
    #     current_dir, "../results/round9/afrobarometer_r9_ghana_latlong_interviewsummary.xlsx"
    # )
    # interview_summary = pd.read_excel(interview_summary_file_path)
    # data = pd.merge(left=data, right=interview_summary[["ID", "interview_summary"]], on="ID")
    ### Configuration for Interview Summary (END) ###

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        # Extract subject backstory
        if include_backstory:
            backstory = f"\n\n{data.loc[i, 'backstory']}"
        else:
            backstory = ""

        # question_prompt = f"{question} Please only respond with 'Yes' or 'No'."
        question_prompt = f"{question}"

        ### Configuration for Step-by-Step Reasoning (START) ###
        #         question_prompt = f"""Please answer the following question by first providing your line of reasoning and then your response using this format: {question}
        #         Reasoning: [Insert your reasoning here]
        #         Response: [Insert your response here]
        #         """

        #         f"""Please answer the following question in the specified format. Start by providing your line of reasoning, followed by a concise and direct response to the question: {question}

        # Expected Format:
        # Reasoning: [Explain your thought process, including any relevant context or logic.]
        # Response: [Provide a clear and concise answer.]"""
        ### Configuration for Step-by-Step Reasoning (END) ###

        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "survey_context": survey_context,
                "demographic_info": generate_qna_format(
                    data.loc[i, demographic_questions],
                    synthetic_experiment=False,  # TODO False if running replication experiment
                )
                + backstory,
                # "demographic_info": data.loc[i, "interview_summary"],
                "question": question,
                "question_prompt": question_prompt,
            }
        )
        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message(
            row["survey_context"], row["demographic_info"]
        ),
        axis=1,
    )

    return prompts


def generate_synthetic_experiment_prompts(
    data: pd.DataFrame,
    survey_context: str,
    demographic_questions: list,
    question: Any,
    include_backstory: bool,
    backstory_file_path: str = "",
) -> pd.DataFrame:
    """
    Generate prompts for synthetic experiment.

    Parameters:
        data (pd.DataFrame): The survey data.
        survey_context (str): The context of the survey.
        demographic_questions (list): The list of demographic questions.
        question (Any): The question to be answered.
        include_backstory (bool): Indicates if the subject's backstory should be included.
        backstory_file_path (str): Indicates the file path to the backstory file

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    if include_backstory:
        # Load backstories
        backstories = pd.read_excel(backstory_file_path)
        data = pd.merge(left=data, right=backstories[["ID", "backstory"]], on="ID")

    if isinstance(question, list):
        question = " ".join(question)

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        # Extract subject backstory
        if include_backstory:
            backstory = f"\n\n{data.loc[i, 'backstory']}"
        else:
            backstory = ""

        # question_prompt = f"{question} Please only respond with 'Yes' or 'No' and then clearly explain the reasoning steps you took that led to your response on a new line:"
        # question_prompt = f"{question} Please only respond with 'Yes' or 'No'."

        # Vaccination Intention
        # question_prompt = f"{question} Please only repond with 'Yes', 'No', 'Do not know', or 'Prefer not to say':"
        # question_prompt = f"{question} Please first provide your reasoning based on the information available to you, then give your final response in the structured format below:\nReasoning: [Your reasoning]\nResponse: [Yes/No/Do not know/Prefer not to say]"

        # Vaccination Outcome
        question_prompt = f"{question} Please give your response to both questions in the structured format below:\nQuestion 1: [Yes/No]\nQuestion 2: [Yes/No]"
        # question_prompt = f"{question} Please first provide your reasoning based on the information available to you, then give your final response to both questions in the structured format below:\nReasoning for Question 1: [Your reasoning]\nResponse for Question 1: [Yes/No]\nReasoning for Question 2: [Your reasoning]\nResponse for Question 2: [Yes/No]"

        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "survey_context": survey_context,
                "demographic_info": generate_qna_format(
                    data.loc[i, demographic_questions],
                    synthetic_experiment=False,
                )
                + backstory,
                "treatment": data.loc[i, "treatment"],
                "question": question,
                "question_prompt": question_prompt,
            }
        )
        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message_with_treatment(
            row["survey_context"], row["demographic_info"], row["treatment"]
        ),
        axis=1,
    )

    return prompts


def generate_candor_synthetic_experiment_prompts(
    data: pd.DataFrame,
    demographic_questions: list,
    question: str,
    include_backstory: bool,
    backstory_file_path: str = "",
    supplementary_file_path: str = "",
) -> pd.DataFrame:
    """
    Generate prompts for synthetic experiment.

    Parameters:
        data (pd.DataFrame): The survey data.
        demographic_questions (list): The list of demographic questions.
        question (str): The question to be answered.
        include_backstory (bool): Indicates if the subject's backstory should be included.
        backstory_file_path (str): Indicates the file path to the backstory file
        supplementary_file_path (str): Indicates the file path to the supplementary country file

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    demographic_questions.remove("country")

    if include_backstory:
        # Load backstories
        backstories = pd.read_excel(backstory_file_path)
        data = pd.merge(left=data, right=backstories[["ID", "backstory"]], on="ID")

    # Load country supplementary data
    supplementary_data = pd.read_excel(supplementary_file_path)
    data = pd.merge(left=data, right=supplementary_data, on="country")

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        # Extract subject backstory
        if include_backstory:
            backstory = f"\n\n{data.loc[i, 'backstory']}"
        else:
            backstory = ""

        question_prompt = f"{question} Please only respond with 'Yes' or 'No' and then clearly explain the reasoning steps you took that led to your response on a new line:"

        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "survey_context": data.loc[i, "synthetic_instruction_prompt"]
                + data.loc[i, "synthetic_highcash_fewshot_demographic"],
                "demographic_info": generate_qna_format(
                    data.loc[i, demographic_questions]
                )
                + backstory,
                "question": question,
                "question_prompt": question_prompt,
                "treatment_transcript": data.loc[i, "highcash_transcript"],
            }
        )
        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message_with_treatment(
            row["survey_context"],
            row["demographic_info"]
            + "\n\nYou were asked to watch the video six weeks ago. Here is the transcript of the video:\n"
            + row["treatment_transcript"],
        ),
        axis=1,
    )

    return prompts


def generate_qna_format(
    demographic_info: pd.Series, synthetic_experiment: bool = False
) -> str:
    """
    Formats the demographic information of a subject in a Q&A format.

    Parameters:
        demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.

    Returns:
        str: The formatted survey response.
    """
    # Shuffle the demographic_info Series
    demographic_info = demographic_info.sample(frac=1)

    survey_response = ""
    counter = 1
    for question, response in demographic_info.items():
        if pd.isnull(response) or response == "NA":
            continue
        survey_response += f"{counter}) Interviewer: {question} Me: {response} "
        counter += 1

    ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (START) ###
    # if synthetic_experiment:
    #     survey_response += f"{counter}) Interviewer: Have you received a vaccination against COVID-19, either one or two doses? Me: No"
    ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (END) ###

    ### Configuration for TB Screening RCT (START) ###
    # if synthetic_experiment:
    #     survey_response += f"{counter}) Interviewer: Have you received a vaccination against Tuberculosis? Me: No"
    ### Configuration for TB Screening RCT (END) ###

    return survey_response


def generate_interview_format(demographic_info: pd.Series) -> str:
    """
    Formats the demographic information of a subject in an interview/interviewee format.

    Parameters:
        demographic_info (pd.Series): A pandas Series containing the demographic information of the subject.

    Returns:
        str: The formatted survey response.
    """
    survey_response = ""
    counter = 1
    for question, response in demographic_info.items():
        if pd.isnull(response):
            continue
        survey_response += (
            f"{counter}) Interviewer: {question} Interviewee: {response} "
        )
        counter += 1

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
            # ### Configuration for Afrobarometer (START) ###
            question_prompts[question] = (
                f'{question} Please only respond with {", ".join([f"{repr(option)}" for option in options[:-1]])} or {repr(options[-1])} and then clearly explain the reasoning steps you took that led to your response on a new line:'
                # f'{question} You must only respond with {", ".join([f"{repr(option)}" for option in options[:-1]])} or {repr(options[-1])}:'
            )
            # ### Configuration for Afrobarometer (END) ###

            ### Configuration for CANDOR (START) ###
            # question_prompts[question] = (
            #     f"{question} Please only respond with 'No' or 'Yes' and then clearly explain the reasoning steps you took that led to your response on a new line:"
            # )
            ### Configuration for CANDOR (END) ###

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
    ### Configuration for Afrobarometer (START) ###

    # Interview Q&A, Interview Summary, Interview + Backstory, Expert Reflection
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}"

    # Interview + Backstory + Vaccination Context
    return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose."

    # Previous strategy
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose.\n\nYou are asked to watch a video at this point. Here is the transcript of the video:\nThe Sun lights up our lives for business for education even for socializing but when the Sun sets many people use candles who are quality battery-operated torches and kerosene lamps as inefficient and expensive ways to create light. What if you can take some Sun with you at night?  You can with portable solar products there are different types, but each portable solar product is made up of three basic parts: a small solar panel, a modern rechargeable battery and an LED bulb. The solar panel catches the light from the Sun and stores this energy in the battery. This can now be used for much needed light when it's dark. Many can even charge phones portable solar products should be reliable affordable and warranted be sure to demand top quality solar products look for these products lighting Africa shining the way."

    # Placebo
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose.\n\nYou are asked to watch a video at this point. Here is the transcript of the video:\n{treatment_video_transcript['Placebo']}"
    # CDC Health
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose.\n\nYou are asked to watch a video at this point. Here is the transcript of the video:\n{treatment_video_transcript['CDC Health']}"
    # Low Cash
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose.\n\nYou are asked to watch a video at this point. Here is the transcript of the video:\n{treatment_video_transcript['Low Cash']}"
    # High Cash
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou should note that the Health officials in Ghana have been communicating extensively to the population – both urban and rural about the COVID-19 virus. Most of the Ghana population know that the COVID-19 virus is dangerous for their health and they are aware of the benefits of getting the COVID-19 vaccination. However, vaccine hesitancy remain a notable challenge, influenced by misinformation and conspiracy theories circulating on social media. Despite efforts by health authorities to promote vaccination, some individuals remained cautious about the safety and efficacy of COVID-19 vaccines. Educational campaigns and outreach efforts are ongoing, but addressing deep-seated concerns and misinformation required continuous effort. Findings from past studies on COVID-19 vaccination efforts in Ghana reveal a complex interplay of factors influencing vaccine uptake and hesitancy. Positive perceptions of vaccines, belief in their efficacy, knowledge of COVID-19, and a generally favorable attitude toward vaccination significantly boost acceptance. Conversely, concerns about negative side effects, mistrust in vaccine safety, fear, and spiritual or religious beliefs contribute to hesitancy. Demographic factors such as educational attainment, gender, religious affiliation, age, and marital status play crucial roles in shaping attitudes towards vaccination. Higher levels of education, female gender, urban residence, Christian affiliation, and reliance on internet sources for COVID-19 information were associated with higher hesitancy rates. Notably, healthcare workers showed a varied acceptance rate influenced by their role, personal connections to COVID-19 cases, and trust in government measures. Despite efforts to increase coverage, only 40% of Ghanaians had received at least one vaccine dose.\n\nYou are asked to watch a video at this point. Here is the transcript of the video:\n{treatment_video_transcript['High Cash']}"
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    # return f"{survey_context}\nYour demographic profile:\n{demographic_prompt}\n\nYou were asked to watch the video six weeks ago. Here is the transcript of the video:\nThe Sun lights up our lives for business for education even for socializing but when the Sun sets many people use candles who are quality battery-operated torches and kerosene lamps as inefficient and expensive ways to create light. What if you can take some Sun with you at night?  You can with portable solar products there are different types, but each portable solar product is made up of three basic parts: a small solar panel, a modern rechargeable battery and an LED bulb. The solar panel catches the light from the Sun and stores this energy in the battery. This can now be used for much needed light when it's dark. Many can even charge phones portable solar products should be reliable affordable and warranted be sure to demand top quality solar products."
    ### Configuration for CANDOR (END) ###


def construct_backstory_system_message(demographic_prompt: str) -> str:
    """
    Constructs system message by combining the survey context and demographic prompt.

    Parameters:
        survey_context (str): The context of the survey.
        demographic_prompt (str): The prompt for demographic information.

    Returns:
        str: The constructed prompt.
    """
    return f"Below you will be asked to complete some demographic questions, and then answer a question. You will see a question from the “Interviewer:” and then your response will be preceded by “Me:”'\n\n{demographic_prompt}"


def construct_system_message_with_treatment(
    survey_context: str, demographic_prompt: str, treatment: str
) -> str:
    """
    Constructs system message by combining the survey context, demographic prompt and treatment prompt.

    Parameters:
        survey_context (str): The context of the survey.
        demographic_prompt (str): The prompt for demographic information.
        treatment (str): The treatment applied to the agent

    Returns:
        str: The constructed prompt.
    """
    ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (START) ###
    return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou are asked to watch a video at this point. Here you are provided with the transcript of the video. You have to read the full transcript in order to continue the survey:\n{treatment_video_transcript[treatment]}"
    ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (END) ###

    ### Configuration for Afrobarometer and TB Screening RCT (START) ###
    # return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nHere is the transcript of the video:\n{treatment_video_transcript[treatment]}"
    ### Configuration for Afrobarometer and TB Screening RCT (END) ###

    ### Configuration for CANDOR (START) ###
    # return f"{survey_context}\nYour demographic profile:\n{demographic_prompt}"
    ### Configuration for CANDOR (END) ###
