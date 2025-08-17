import os
import pandas as pd
from src.data_processing import load_data, include_variable_names
from src.prompt_generation import (
    generate_prompt_strategy_evaluation_prompts,
)
from src.api_interaction import (
    inference_endpoint_query,
)


def main(request):
    # Load and preprocess data
    data = load_data(data_file_path, drop_first_row=drop_first_row)

    # Generate demographic prompts
    prompts = generate_prompt_strategy_evaluation_prompts(
        data,
        request["survey_context"],
        request["question"],
        prompt_strategy=strategy,
    )

    # Perform query for survey questions
    prompts_with_responses = inference_endpoint_query(
        endpoint_url=request["api_url"],
        prompts=prompts,
        system_message_field="system_message",
        user_message_field="question_prompt",
        experiment_round=request["experiment_round"],
        experiment_version=version,
        model_name=request["model_name"],
    )

    data_with_responses = pd.merge(
        left=data,
        right=prompts_with_responses,
        on="ID",
        suffixes=("", "_y"),
    )

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
    # ### Configuration for COVID-19 Vaccination RCT (START) ###
    strategy = "expertreflections"  # backstories, interviewsummary, expertreflections
    with_intention = True
    version = f"vaccine_financial_incentive_vaccinationstatus_llama3.1_8b_s1_{strategy}"  # Vaccination Outcome
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "S1 (Instruct Model)"
    model = "Llama 3.1 8B"
    data_file_path = os.path.join(
        current_dir,
        "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
    )  # Vaccination Outcome
    treatment_assignment_column = "treatment"
    api_url = ""  # HF dedicated inference endpoint
    model_name = "together"  # huggingface, together
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
        "treatment_assignment_column": treatment_assignment_column,
        "api_url": api_url,
        "model_name": model_name,
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
        ],
        "question": [
            "Have you received a COVID-19 vaccine?",
            "Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?",
        ],
        "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, social media use, and vaccination intention. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video and receive further information on the vaccination intention of your human subject. Thereafter, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    }

    if with_intention:
        input_data["demographic_questions"] += [
            "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
            "Why will you NOT get vaccinated against COVID-19?",
            "We understand that there is always some uncertainty regarding all decisions. From 0% to 100%, what do you think are the chances that you will choose to get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? - 4",
        ]
    # ### Configuration for COVID-19 Vaccination RCT (END) ###

    main(input_data)
