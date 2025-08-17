import os
import pandas as pd
from src.data_processing import load_data, create_batch_file, include_variable_names
from src.prompt_generation import generate_synthetic_experiment_prompts
from src.api_interaction import batch_query
from openai import OpenAI
from config.settings import OPENAI_API_KEY


def main(request):
    # Load OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    # Load and preprocess data
    data = load_data(data_file_path, drop_first_row=drop_first_row)

    # Generate demographic prompts
    prompts = generate_synthetic_experiment_prompts(
        data,
        request["survey_context"],
        request["demographic_questions"],
        request["question"],
        study=request["study"],
    )

    # Perform batch query for survey questions
    batch_file_dir = create_batch_file(
        prompts,
        system_message_field="system_message",
        user_message_field="question_prompt",
        batch_file_name="batch_input_llm_replication_experiment.jsonl",
    )

    llm_responses = batch_query(
        client,
        batch_input_file_dir=batch_file_dir,
        batch_output_file_dir="batch_output_llm_replication_experiment.jsonl",
    )

    llm_responses.rename(columns={"query_response": "llm_response"}, inplace=True)

    prompts_with_responses = pd.merge(left=prompts, right=llm_responses, on="custom_id")
    data_with_responses = pd.merge(
        left=data, right=prompts_with_responses, on="ID", suffixes=("", "_y")
    )

    # For Vaccination Intent
    # data_with_responses["user_response"] = data_with_responses[request["question"]]

    # For Vaccination Outcome
    data_with_responses["user_response"] = data_with_responses[request["question"][0]]
    data_with_responses["user_response_2"] = data_with_responses[request["question"][1]]

    # Include model and experiment information
    data_with_responses["model"] = model
    data_with_responses["scenario"] = scenario

    # Include variable names as new column headers
    if drop_first_row:
        data_with_response_headers = include_variable_names(
            data_with_responses, data_file_path
        )

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/{request['experiment_round']}/{version}.xlsx"
    )
    data_with_response_headers.to_excel(prompts_response_file_path, index=False)


if __name__ == "__main__":
    # version = "vaccine_financial_incentive_vaccinationintention_gpt4o_predicttreatmenteffects"  # Vaccination Intent
    version = "vaccine_financial_incentive_vaccinationstatus_gpt4o_predicttreatmenteffects"  # Vaccination Outcome
    study = "duch_2023"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "Predicting Treatment Effects"
    model = "GPT 4o"
    # data_file_path = os.path.join(
    #     current_dir,
    #     "../data/duch_et_al_2023_vaccine_financial_vaccine_intention_training.csv",
    # )  # Vaccination Intention
    data_file_path = os.path.join(
        current_dir,
        "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
    )  # Vaccination Outcome
    backstory_file_path = ""
    treatment_assignment_column = "treatment"
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
        "study": study,
        "treatment_assignment_column": treatment_assignment_column,
        "experiment_round": experiment_round,
        "demographic_questions": [
            "Start Date",
            "What is your current age?",
            "What is your gender?",
            "What is the highest educational qualification you have completed?",
            "Which region do you live in?",
            "Which distric do you live in?",
            "What is the name of the community you live in?",
            "How many people live in your village?",
            "What is the distance in km of the nearest health clinic from where you live?",
            "How many people live in the house together with you (NOT including you) at this moment?",
            "How many children below 18 years old are currently living in your home?",
            "What is your current working situation?",
            "How much (in Ghanaian Cedis) on average does your household spend in a typical week on food?",
            "How much (in Ghanaian Cedis) on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
            "How would you rate the overall economic or financial condition of your household today?",
            "Do you have a registered mobile number?",
            "How many family members do you have in another village?",
            "How many friends and acquaintances who are not part of your family do you have in another village?",
            "How many individuals can you identify in your social network? Think of friends and relatives that live close to you",
            "How often do you use social media?",
            # Only for Vaccination Outcome
            "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
            "Why will you NOT get vaccinated against COVID-19?",
            "We understand that there is always some uncertainty regarding all decisions. From 0% to 100%, what do you think are the chances that you will choose to get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? - 4",
        ],
        # Vaccination intent
        # "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
        # "survey_context": "You will be asked to predict how people respond to various video messages. Social scientists often conduct research studies using online surveys. The text below is from one such survey conducted on a large, diverse population in Ghana.\nWe are researchers from the University of Ghana and the University of Oxford, United Kingdom, conducting a study on COVID-19 vaccines. The project is led by Dr. Edward Asiedu of the University of Ghana, working in collaboration with Professor Philip Clarke and Professor Raymond Duch from the University of Oxford, and their team of researchers to better understand vaccine uptake. We very much appreciate your interest in participating in this study. You will be asked some questions about yourself. This should take about 5 minutes. No background knowledge is required. The information that we gather from this study will be used to understand more about COVID-19 vaccinations.",
        # Vaccination Outcome
        "question": [
            "Have you received a COVID-19 vaccine?",
            "Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?",
        ],
        "survey_context": "You will be asked to predict how people respond to various video messages. Social scientists often conduct research studies using online surveys. The text below is from one such survey conducted on a large, diverse population in Ghana.\nWe are researchers from the University of Ghana and the University of Oxford, United Kingdom, conducting a study on COVID-19 vaccines. The project is led by Dr. Edward Asiedu of the University of Ghana, working in collaboration with Professor Philip Clarke and Professor Raymond Duch from the University of Oxford, and their team of researchers to better understand vaccine uptake. We very much appreciate your interest in participating in this study. You will be asked some questions about yourself. This should take about 5 minutes. No background knowledge is required. The information that we gather from this study will be used to understand more about COVID-19 vaccinations.",
    }
    ### Configuration for COVID-19 Vaccination RCT (END) ###

    main(input_data)
