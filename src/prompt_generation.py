import pandas as pd
import os
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

duch_2023_treatments = {
    "CDC Health": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID 19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. Getting the COVID-19 vaccine will help prevent you from getting COVID-19 and reduce your risk of being hospitalized with COVID-19. COVID 19 vaccine help you to protect yourself your environment and your loved ones from COVID-19 exposure.\n\nWe indicated that we will follow up with you in 6 weeks. We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification",
    "Placebo": "The Sun lights up our lives for business for education even for socializing but when the Sun sets many people use candles who are quality battery-operated torches and kerosene lamps as inefficient and expensive ways to create light. What if you can take some Sun with you at night?  You can with portable solar products there are different types, but each portable solar product is made up of three basic parts: a small solar panel, a modern rechargeable battery and an LED bulb. The solar panel catches the light from the Sun and stores this energy in the battery. This can now be used for much needed light when it's dark. Many can even charge phones portable solar products should be reliable affordable and warranted be sure to demand top quality solar products look for these products lighting Africa shining the way.\n\nWe indicated that we will follow up with you in 6 weeks. We will contact you in order to verify your vaccination status.  If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification.",
    "Low Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 20 Cedi. If you get vaccinated, you will get rewarded.\n\nWe indicated that we will follow up with you in 30 days.  We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification and you will be paid your 20 Cedi via cell phone money payment or by cash if you prefer.",
    "High Cash": "Health authorities are working hard to distribute the COVID-19 vaccines free for everyone with no strings attached. COVID-19 vaccines are safe and effective. After you have been fully vaccinated you can resume activities that you did prior to the pandemic. If you have at least one COVID-19 vaccine shot you will receive 60 Cedi. If you get vaccinated, you will get rewarded.\n\nWe indicated that we will follow up with you in 6 weeks.  We will contact you in order to verify your vaccination status. If you can provide us with your COVID-19 vaccination carnet at the time, we will upload a copy of the vaccination carnet to our secure server for verification and you will be paid your 60 Cedi via cell phone money payment or by cash if you prefer.",
}

duch_2025_treatments = {
    "tbhealth": "Health authorities are working hard to test people for being at risk of getting ill with tuberculosis. If you are at risk you will be treated to stop you getting ill with tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from tuberculosis. One in four people have sleeping tuberculosis. If you have sleeping tuberculosis, you will feel well, but there is a risk that the tuberculosis bacteria will wake up and give you active tuberculosis, a serious illness. Getting tested and treated for sleeping tuberculosis will prevent you from getting active tuberculosis and reduce your risk of being hospitalized with tuberculosis. Tuberculosis testing will help you to protect yourself and your environment and your loved ones from tuberculosis exposure.",
    "tbhealthplus3": "Health authorities are working hard to test people for being at risk of getting ill with tuberculosis. If you are at risk you will be treated to stop you getting ill with tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from tuberculosis. If you show up for the scheduled tuberculosis testing in your village and get the tuberculosis test you will receive 20 Cedi. If you get tuberculosis tested, you will get rewarded.",
    "tbhealthplustext": "Health authorities are working hard to test people for being at risk of getting ill with tuberculosis. If you are at risk you will be treated to stop you getting ill with tuberculosis. The tests and treatment are safe and effective and free for everyone with no strings attached. After you have been tested and treated you will be safe from tuberculosis. One in four people have sleeping tuberculosis. If you have sleeping tuberculosis, you will feel well, but there is a risk that the tuberculosis bacteria will wake up and give you active tuberculosis, a serious illness. Getting tested and treated for sleeping tuberculosis will prevent you from getting active tuberculosis and reduce your risk of being hospitalized with tuberculosis. Tuberculosis testing will help you to protect yourself and your environment and your loved ones from tuberculosis exposure. You also received a telephone call reminding you to go for your tuberculosis screening appointment.",
}

campos_treatments = {
    "Control": "We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nReminder\nThank you again for participating in the survey on COVID-19 vaccination.\nWe would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally\nwithin the first 30 days after the vaccine becomes available to you.\n\nAt the end of the survey you are also provided with a link to get information about how you can book an appointment for vaccination against COVID-19 in your region.\n\nYou received two reminders to get vaccinated, sent 2 and 4 weeks after taking the survey.",
    "Incentives": "We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nWe offer you SEK 200 if you get a first shot of a COVID-19 vaccine within the first 30 days after the vaccination becomes available to you*.\n\n* available means that vaccination started for people in your age category and region. If the vaccine has already become available to you, you will receive the SEK 200 if you get vaccinated within 30 days. We will pay you as soon as possible, but latest before the end of the year.\n\nWe will check with the public health agency whether you vaccinated within 30 days the vaccine has become available to you. If you got vaccinated, we will send you a gift card with a value of SEK 200. As explained previously, your data will be treated confidentially. The following picture is a certificate that ensures that you will be paid SEK 200 if you get a COVID-19 vaccine within 30 days after it becomes available to you. Please take a picture and/or save this document.\n\nReminder\nThank you again for participating in the survey on COVID-19 vaccination. We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you. Remember that we will pay you SEK 200 if you get a first shot of a COVID-19 vaccine within one month after which it became available to you.\n\nAt the end of the survey you are also provided with a link to get information about how you can book an appointment for vaccination against COVID-19 in your region.\n\nYou received two reminders to get vaccinated, sent 2 and 4 weeks after taking the survey.",
    "Social Benefit": "We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nThe COVID-19 vaccine not only protects you, but also protects people around you (e.g., family, friends, neighbors, work colleagues, and local shopkeepers). Now, we would like you to make a list of the 4 people who will benefit if you get the vaccine.\n\nIn this part of the survey you are asked to write down their first name (if you know the person’s name) and how they are related to you. Note that none of this information will be matched with your personal data.\nAs an example, please take a look at the list of Erik Wengström, co-researcher of this study:\nAnn, Mother\nAnders, Friend in a risk group\nMohammed, My local pizza cook\nJohan and his schoolmates, Students in the local high school\n\nReminder\nThank you again for participating in the survey on COVID-19 vaccination. We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nWe would like to remind you that the COVID-19 vaccine not only protects you, but also protects the people around you (e.g., family, neighbors, work colleagues, and local shopkeepers). When you participated in our survey, you made a list consisting of four people that would benefit if you took the vaccine. We would like that you think about these four people when you consider taking the vaccine.\n\nAt the end of the survey you are also provided with a link to get information about how you can book an appointment for vaccination against COVID-19 in your region.\n\nYou received two reminders to get vaccinated, sent 2 and 4 weeks after taking the survey.",
    "Argument": "We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nThere are people who do not plan to get the vaccine soon after it becomes available for them. We would like to ask you to write down arguments that you think could best convince another person to change his/her mind and get the vaccine as soon as possible, ideally within 30 days after it becomes available to him/her.\n\nWe will also give you the opportunity to share your argument with a person that does not plan to get the vaccine. We will randomly select the arguments of ten participants in this study and control that the participant agreed to share the argument. If the participant agreed, we will then share the argument with a person that does NOT plan to get the vaccine and does NOT have an increased risk of side effects from COVID-19 vaccination. You remain anonymous and your argument will never be connected to your personal data. Note: You can write down an argument directly. Alternatively, you are also welcome to look for arguments, for example on the Swedish health authority website.\n\nReminder\nThank you again for participating in the survey on COVID-19 vaccination. We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nWe would like to remind you that you wrote an argument to convince another person to take the vaccine as soon as possible, ideally within the first 30 days after it becomes available to them. We would like you to think about an argument that you think could best convince another person to get the vaccine.\n\nAt the end of the survey you are also provided with a link to get information about how you can book an appointment for vaccination against COVID-19 in your region.",
    "Information": "We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nIn the following, we are asked to fill out a short quiz about the effectiveness and safety of the COVID-19 vaccine.\n\nThereafter we are provided with the following information.\n\nThe information below is confirmed by the virologist Prof. Niklas Arnberg at Umeå University:\nTrials have shown that the currently approved vaccines in Sweden strongly protect against the virus. In fact, results from millions of vaccinated people in Israel show that the Pfizer-BioNTech vaccine prevents 97% of deaths from COVID-19.\n\nThe information below is confirmed by the virologist Prof. Niklas Arnberg at Umeå University:\n\nThe vaccines have shown to be safe.\n\nSerious side-effects are very rare. The vaccines that are used in Sweden for your age group can rarely create side effects in the form of allergic reactions. Studies indicate that fewer than 3 people per 10,000 vaccinated get such an effect. Most of them have previously had allergies, and everyone in the studies recovered himself/herself completely.\n\nAfter more than half of USAs adult population has vaccinated\n\nThe vaccines only very rarely trigger side-effects in the form of allergic (anaphylactic) reactions in 5 to 10 people out of 1,000,000 vaccinated people or in 0.001% of vaccinated people. Most people who developed these reactions have had a history of allergies, and all of them have fully recovered.\n\nAfter more than half of the US adult population has been vaccinated, no causal link has been established between deaths and the vaccines used in Sweden for your age group. Within the EU, over 120 million doses of the Pfizer-BioNTech vaccine have been administered. Here, too, no link has been established between deaths and the vaccine.\n\nReminder\nThank you again for participating in the survey on COVID-19 vaccination. We would like to encourage you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you.\n\nIn the study, we asked two questions about the efficacy and safety of the COVID-19 vaccines. Based on the studies we referred to, the following applies:\n\nThe vaccines are very effective. The COVID-19 vaccines used in Sweden for your age group have been shown to reduce COVID-19 deaths by 97%.\n\nThe vaccines have been shown to be safe. After more than 300 million vaccinated people in the EU and the US, no link has been established between deaths and the vaccines used for your age group.\n\nAt the end of the survey you are also provided with a link to get information about how you can book an appointment for vaccination against COVID-19 in your region.\n\nYou received two reminders to get vaccinated, sent 2 and 4 weeks after taking the survey.",
    "No reminders": "",
}

milkman_treatments = {
    "Control": "",
    "Baseline": "In your area, an initiative was implemented that consisted in CVS Pharmacy sending text messages in early November 2022 to encourage adoption of the bivalent COVID-19 booster.\n\nThis is the text message that you received.\n\nCVS Pharmacy: Hi [Patient First Name]! Updated COVID boosters are recommended to help prevent infection & severe illness. Your booster is waiting for you at CVS.\n\nSchedule: cvs.co/8981004\n\nThis is the reminder text message that you received 7 days after the first message.\n\nCVS Pharmacy: Remember, a COVID booster is waiting for you at CVS. Schedule: cvs.co/9810048",
    "Free ride": "In your area, an initiative was implemented that consisted in CVS Pharmacy sending text messages in early November 2022 to encourage adoption of the bivalent COVID-19 booster.\n\nThis is the text message that you received.\n\nCVS Pharmacy: Hi [Patient First Name]! Updated COVID boosters are recommended to help prevent infection & severe illness. Your booster is waiting for you at CVS.\n\nA free ride to and from CVS has been reserved for your booster appointment until 8 December 2022 with support from the Mercury Project. Schedule: cvs.co/8747314\n\nYou can claim your free rides to or from any CVS near you by entering your personal code VAXBR4QKHVQBRKLM in the Lyft app https://lyft.com/lp/VAXBR4QKHVQBRKLM\n\nThis is the reminder text message that you received 7 days after the first message.\n\nCVS Pharmacy: Remember, a COVID booster is waiting for you at CVS. Schedule: cvs.co/7473148\n\nAs a reminder, a free ride to and from CVS has been reserved for your booster appointment until 12/8/22 with support from the Mercury Project.\n\nYou can claim your free rides to or from any CVS near you by entering your personal code VAXBR4QKHVQBRKLM in the Lyft app https://lyft.com/lp/VAXBR4QKHVQBRKLM",
}


def generate_formatting_prompts(
    data: pd.DataFrame,
    formatting_prompt: str,
) -> pd.DataFrame:
    """
    Generates a DataFrame of formatting prompts for each row in the input data.

    For each row in the input DataFrame, this function creates a dictionary containing:
        - 'custom_id': a unique identifier for the prompt (as a string).
        - 'ID': the original ID from the input data.
        - 'system_message': the provided formatting prompt string.
        - 'question_prompt': the value from the 'llm_response' column, or an empty string if it is null.

    Args:
        data (pd.DataFrame): Input DataFrame containing at least 'ID' and 'llm_response' columns.
        formatting_prompt (str): The system message to be used for formatting.

    Returns:
        pd.DataFrame: A DataFrame containing the generated prompts with columns:
            'custom_id', 'ID', 'system_message', and 'question_prompt'.
    """
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        if pd.isnull(data.loc[i, "llm_response"]):
            question_prompt = ""
        else:
            question_prompt = data.loc[i, "llm_response"]
        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "system_message": formatting_prompt,
                "question_prompt": question_prompt,
            }
        )

        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    return prompts


def generate_demographic_prompts(
    data: pd.DataFrame,
    demographic_questions: list,
    system_message: str,
    question_prompt: str,
) -> pd.DataFrame:
    """
    Generate prompts for creating demographic prompts using different prompt engineering strategies.

    Parameters:
        data (pd.DataFrame): The survey data.
        demographic_questions (list): The list of demographic questions.
        system_message (str): The system message to be used in the prompts.
        question_prompt (str): The question prompt to be used in the prompts.

    Returns:
        pd.DataFrame: The prompts generated for creating backstories for each user.
    """
    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        demographic_info = generate_interview_format(data.loc[i, demographic_questions])
        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "demographic_info": demographic_info,
                "system_message": system_message.format(
                    demographic_info=demographic_info
                ),
                "question_prompt": question_prompt,
            }
        )
        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    return prompts


def generate_prompt_strategy_evaluation_prompts(
    data: pd.DataFrame,
    survey_context: str,
    question: str,
    prompt_strategy: str,
) -> pd.DataFrame:
    """
    Generate prompts for synthetic experiment.

    Parameters:
        data (pd.DataFrame): The survey data.
        survey_context (str): The context of the survey.
        question (str): The question to be answered.
        prompt_strategy (str):  The prompt strategy to be used for generating demographic prompts.

    Returns:
        pd.DataFrame: The prompts generated for each question for each user.
    """
    current_dir = os.path.dirname(__file__)

    if prompt_strategy == "backstories":
        demographics_file_path = os.path.join(
            current_dir,
            "../results/round9/vaccine_financial_incentive_vaccinationstatus_backstories.xlsx",
        )
        demographics = pd.read_excel(demographics_file_path)
        data = pd.merge(left=data, right=demographics[["ID", "backstory"]], on="ID")
        data.rename(columns={"backstory": "demographic_prompt"}, inplace=True)

    elif prompt_strategy == "interviewsummary":
        demographics_file_path = os.path.join(
            current_dir,
            "../results/round9/vaccine_financial_incentive_vaccinationstatus_interviewsummary.xlsx",
        )
        demographics = pd.read_excel(demographics_file_path)
        data = pd.merge(
            left=data, right=demographics[["ID", "interview_summary"]], on="ID"
        )
        data.rename(columns={"interview_summary": "demographic_prompt"}, inplace=True)

    elif prompt_strategy == "expertreflections":
        expert_roles = [
            "psychologist",
            "economist",
            "politicalscientist",
            "demographer",
        ]
        for role in expert_roles:
            demographics_file_path = os.path.join(
                current_dir,
                f"../results/round9/vaccine_financial_incentive_vaccinationstatus_expertreflections_{role}.xlsx",
            )
            demographics = pd.read_excel(demographics_file_path)
            data = pd.merge(
                left=data, right=demographics[["ID", "expert_reflection"]], on="ID"
            )
            data.rename(
                columns={"expert_reflection": f"expert_reflection_{role}"}, inplace=True
            )

        data["expert_reflection"] = data.apply(
            lambda row: f"{row['expert_reflection_psychologist']}\n\n{row['expert_reflection_economist']}\n\n{row['expert_reflection_politicalscientist']}\n\n{row['expert_reflection_demographer']}",
            axis=1,
        )
        data.rename(columns={"expert_reflection": "demographic_prompt"}, inplace=True)

    else:
        raise ValueError(
            "Invalid prompt strategy. Choose from 'backstories', 'interviewsummary' or 'expertreflections'."
        )

    if isinstance(question, list):
        question = ". ".join(question)

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        # Vaccination Outcome
        question_prompt = f"{question} Please give your response to both questions in the structured format below:\nQuestion 1: [Yes/No]\nQuestion 2: [Yes/No]"

        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "survey_context": survey_context,
                "demographic_info": data.loc[i, "demographic_prompt"],
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


def generate_synthetic_experiment_prompts(
    data: pd.DataFrame,
    survey_context: str,
    demographic_questions: list,
    question: Any,
    study: str = "duch_2023",
) -> pd.DataFrame:
    """
    Generates synthetic experiment prompts for each participant in a survey dataset, tailored to the specified study design.
    Args:
        data (pd.DataFrame): DataFrame containing survey participant data, including demographic information, treatment assignment, and optional backstory.
        survey_context (str): Context or description of the survey to be included in the prompt.
        demographic_questions (list): List of column names in `data` representing demographic questions to be formatted.
        question (Any): The main survey question(s) to be included in the prompt. Can be a string or a list of strings.
        study (str, optional): The study design to use for prompt formatting. Supported values are "duch_2023", "duch_2025", "milkman_baseline", "milkman_control", and "campos". Defaults to "duch_2023".
    Returns:
        pd.DataFrame: DataFrame containing generated prompts for each participant, including custom ID, survey context, demographic info, treatment, question, question prompt, and system message.
    Raises:
        ValueError: If an unsupported study type is provided.
    """
    if isinstance(question, list):
        question = " ".join(question)

    # Iterate through the survey data and generate prompts for each question for each user
    prompts = []
    custom_id_counter = 0
    for i in range(len(data)):
        if study == "milkman_baseline":
            # Milkman
            question_prompt = "Did you receive a COVID-19 booster shot within 30 days after getting the first message from the CVS Pharmacy? Please give your response to the question in the structured format below:\nQuestion: [Yes/No]"  # Baseline + Free ride

        elif study == "milkman_control":
            # Milkman
            question_prompt = "Did you receive a COVID-19 booster by early December 2022, within the first 30 days after the information on your profile was collected? Please give your response to the question in the structured format below:\nQuestion: [Yes/No]"  # Control

        elif study == "campos":
            # Campos Mercade RCT
            question_prompt = f"{question} Please give your response to the question in the structured format below:\nQuestion: [Yes/No]"

        elif study == "duch_2023":
            # Vaccination Outcome
            question_prompt = f"{question} Please give your response to both questions in the structured format below:\nQuestion 1: [Yes/No]\nQuestion 2: [Yes/No]"

        elif study == "duch_2023_synthetic":
            # Vaccination Outcome
            question_prompt = f"{question} Please give your response to the question in the structured format below:\nQuestion: [Yes/No]"

        elif study == "duch_2025":
            # TB Screening
            question_prompt = f"{question} Please give your response to both questions in the structured format below:\nQuestion 1: [Yes/No/Do not know/Prefer not to say]\nQuestion 2: [Yes/No]"

        else:
            raise ValueError(f"Study {study} not supported.")

        prompts.append(
            {
                "custom_id": f"{custom_id_counter}",
                "ID": data.loc[i, "ID"],
                "survey_context": survey_context,
                "demographic_info": generate_qna_format(
                    data.loc[i, demographic_questions]
                ),
                "treatment": data.loc[i, "treatment"],
                "question": question,
                "question_prompt": question_prompt,
            }
        )
        custom_id_counter += 1
    prompts = pd.DataFrame(prompts)

    prompts["system_message"] = prompts.apply(
        lambda row: construct_system_message_with_treatment(
            row["survey_context"],
            row["demographic_info"],
            row["treatment"],
            study=study,
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
    # Shuffle the demographic_info Series
    demographic_info = demographic_info.sample(frac=1)

    survey_response = ""
    counter = 1
    for question, response in demographic_info.items():
        if pd.isnull(response) or response == "NA":
            continue

        if type(response) == str and "\n" in response:
            response = response.split("\n")[0].replace("\r", "")

        survey_response += f"{counter}) Interviewer: {question} Me: {response} "
        counter += 1

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


def construct_system_message_with_treatment(
    survey_context: str, demographic_prompt: str, treatment: str, study: str
) -> str:
    """
    Constructs system message by combining the survey context, demographic prompt and treatment prompt.

    Parameters:
        survey_context (str): The context of the survey.
        demographic_prompt (str): The prompt for demographic information.
        treatment (str): The treatment applied to the agent
        study (str): The study type of interest

    Returns:
        str: The constructed prompt.
    """
    if study in ["milkman_baseline", "milkman_control"]:
        ### Configuration for Milkman et al RCT (START) ###
        return f"{survey_context}\n\nYour demographic profile based on information collected:\n{demographic_prompt}\n\n{milkman_treatments[treatment]}"
        ### Configuration for Milkman et al RCT (END) ###

    elif study in ["duch_2023", "duch_2023_synthetic"]:
        ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (START) ###
        return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nYou are asked to watch a video at this point. Here you are provided with the transcript of the video. You have to read the full transcript in order to continue the survey:\n{duch_2023_treatments[treatment]}"
        ### Configuration for Afrobarometer and COVID-19 Vaccination RCT (END) ###

    elif study == "campos":
        ### Configuration for Campos Mercade RCT (START) ###
        return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\n{campos_treatments[treatment]}"
        ### Configuration for Campos Mercade RCT (END) ###

    elif study == "duch_2025":
        ### Configuration for TB Screening RCT (START) ###
        return f"{survey_context}\n\nYour demographic profile:\n{demographic_prompt}\n\nIn your area, an initiative was implemented that consisted in bringing pop-up tuberculosis clinics in several villages - including yours - so that most villagers could walk to the clinics within minutes.\n\nWhen you were informed of the initiative, you were also presented with a video message. Here is the transcript of the video:\n{duch_2025_treatments[treatment]}"
        ### Configuration for TB Screening RCT (END) ###

    else:
        raise ValueError(f"Study {study} is not supported.")
