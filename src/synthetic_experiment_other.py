import os
import pandas as pd
from src.data_processing import load_data, include_variable_names
from src.prompt_generation import (
    generate_synthetic_experiment_prompts,
    generate_replication_experiment_prompts,
    generate_candor_synthetic_experiment_prompts,
)
from src.api_interaction import (
    inference_endpoint_query,
)


def main(request):
    # Load and preprocess data
    data = load_data(data_file_path)
    # cols_of_interest = ["ID"] + request["demographic_questions"] + [request["question"]]  # TODO replication experiment
    cols_of_interest = ["ID"] + request[
        "demographic_questions"
    ]  # TODO synthetic experiment

    # Generate demographic prompts
    ### Configuration for Afrobarometer (START) ###
    # prompts = generate_replication_experiment_prompts(
    #     data,
    #     request["survey_context"],
    #     request["demographic_questions"],
    #     request["question"],
    #     include_backstory=True,  # True if backstory should be included
    #     backstory_file_path=request["backstory_file_path"],
    # )
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    # prompts = generate_candor_synthetic_experiment_prompts(
    #     data,
    #     request["demographic_questions"],
    #     request["question"],
    #     include_backstory=True,  # True if backstory should be included
    #     backstory_file_path=request["backstory_file_path"],
    #     supplementary_file_path=request["supplementary_file_path"]
    # )
    ### Configuration for CANDOR (END) ###

    ### Configuration for COVID-19 Vaccination RCT (START) ###
    data["treatment"] = treatment
    prompts = generate_synthetic_experiment_prompts(
        data,
        request["survey_context"],
        request["demographic_questions"],
        request["question"],
        include_backstory=False,  # True if backstory should be included
        backstory_file_path=request["backstory_file_path"],
    )
    ### Configuration for COVID-19 Vaccination RCT (END) ###

    ### Configuration for HuggingFace and Deepseek (START) ###
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
    ### Configuration for HuggingFace and Deepseek (END) ###

    data_with_responses = pd.merge(
        left=data[cols_of_interest], right=prompts_with_responses, on="ID"
    )
    data_with_responses["user_response"] = data_with_responses[request["question"]]

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
    ### Configuration for Afrobarometer (START) ###
    # version = "afrobarometer_replication_gemma-2-27b_s2"
    # # version = "afrobarometer_synthetic_placebo_llama-3.1-8b_s3"
    # experiment_round = "round8"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/afrobarometer.xlsx")
    # backstory_file_path = os.path.join(
    #     current_dir, f"../results/{experiment_round}/afrobarometer_backstory.xlsx"
    # )
    # api_url = ""

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "api_url": api_url,
    #     "experiment_round": experiment_round,
    #     "demographic_questions": [
    #         "Do you come from a rural or urban area?",
    #         "How old are you?",
    #         "What is your gender?",
    #         "What is your highest level of education?",
    #         "What is your religion, if any?",
    #         "Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job?",
    #         "What region do you come from?",
    #         "Do you feel close to any particular political party?",
    #         "When you get together with your friends or family, how often would you say you discuss political matters?",
    #         "Latitude",
    #         "Longitude",
    #         "What is the distance to the nearest health clinic from your location in kilometers?",
    #         "What district do you live in?",
    #         "What percentage of the population in your district voted for the National Democratic Congress (NDC)?",
    #         "What percentage of the population in your district voted for the New Patriotic Party (NPP)?",
    #         "In the past 12 months, have you had contact with a public clinic or hospital?",
    #     ],
    #     "question": "Have you received a vaccination against COVID-19, either one or two doses?",
    #     "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    #     # "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
    #     # "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked about your intentions to receive the COVID-19 vaccine. Assume that you have not been vaccinated against COVID-19. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # }
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    # version = "candor_synthetic_backstory+cotreasoning_highcash_sample_600"
    # current_dir = os.path.dirname(__file__)
    # experiment_round = "round8"
    # data_file_path = os.path.join(current_dir, "../data/candor_sample_600.xlsx")
    # backstory_file_path = os.path.join(current_dir, f"../results/{experiment_round}/candor_backstory_5countries.xlsx")
    # supplementary_file_path = os.path.join(current_dir, f"../results/{experiment_round}/candor_supplementary.xlsx")

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "supplementary_file_path":supplementary_file_path,
    #     "demographic_questions": [
    #         'What is your gender?',
    #         'What is your age?',
    #         "The following is a scale from 0 to 10 that goes from left to right, where 0 means 'Left' and 10 means 'Right'. Today when talking about political trends, many people talk about those who are more sympathetic to the left or the right. According to the sense that the terms 'Left' and 'Right' have for you when you think about your political point of view, where would you find yourself on this scale?",
    #         'Gross HOUSEHOLD income combines your gross income with that of your partner or any other household member with whom you share financial responsibilities BEFORE any taxes are paid and BEFORE any benefits are obtained. What is your gross annual household income?',
    #         'Thinking back to 12 months ago, has your household income increased or decreased since then?',
    #         'We would like to know how good or bad your health is TODAY. How would you rate your health today on a scale numbered 0 to 100? 100 means the best health you can imagine. 0 means the worst health you can imagine.',
    #         'What is the highest degree or level of education you have completed?',
    #         'Do you have any dependent children who live with you? (By "dependent" children, we mean those who are not yet financially independent).',
    #         'Are you currently married, in a civil partnership, or living with a partner?',
    #         'Would you vote to re-elect this government in the next election?',
    #         'Overall, how would you rate the current government on a scale of 0 (very low rating) to 100 (very high rating)?',
    #         'Where in the country do you live?',
    #         'country'
    #     ],
    #     # "question":"Since you watched this video six weeks ago, do you think you will get a first shot of a COVID-19 vaccine if the vaccine becomes available to you?",
    #     "question":"You watched this video six weeks ago. Think about the content of the video and consider all the information you have been given. Between six weeks ago and now did you receive a COVID-19 vaccine?",

    #     "survey_context":""
    # }
    ### Configuration for CANDOR (END) ###

    ### Configuration for COVID-19 RCT (START) ###
    version = "covid19_rct_synthetic_instruct_XXX"
    # version = "covid19_rct_synthetic_instructiontuned_XXX"
    # version = "covid19_rct_synthetic_healthcaretuned_XXX"
    # version = "covid19_rct_synthetic_rcttuned_XXX"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    data_file_path = os.path.join(current_dir, "../data/covid_vaccination_rct.csv")
    backstory_file_path = ""
    treatment = ""
    api_url = "https://api.deepseek.com"
    model_name = "Deepseek"  # huggingface, deepseek, claude, gemini,
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
        "backstory_file_path": backstory_file_path,
        "api_url": api_url,
        "model_name": model_name,
        "experiment_round": experiment_round,
        "demographic_questions": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        "question": "",
        "survey_context": "",
    }
    ### Configuration for COVID-19 RCT (END) ###

    main(input_data)
