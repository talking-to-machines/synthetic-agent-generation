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
    data = load_data(data_file_path, drop_first_row=drop_first_row)
    # cols_of_interest = (
    #     ["ID"] + request["demographic_questions"] + [request["question"]]
    # )  # TODO replication experiment
    # cols_of_interest = ["ID"] + request[
    #     "demographic_questions"
    # ]  # TODO synthetic experiment

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

    ### Configuration for COVID-19 Vaccination RCT and TB Screening RCT (START) ###
    prompts = generate_synthetic_experiment_prompts(
        data,
        request["survey_context"],
        request["demographic_questions"],
        request["question"],
        include_backstory=False,  # True if backstory should be included
        backstory_file_path=request["backstory_file_path"],
    )
    ### Configuration for COVID-19 Vaccination RCT and TB Screening RCT (END) ###

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

    # For Vaccination Intent
    # data_with_responses["user_response"] = data_with_responses[request["question"]]

    # For Vaccination Outcome and TB Vaccination
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

    ### Configuration for COVID-19 Vaccination RCT (START) ###
    # version = "vaccine_financial_incentive_vaccinationintention_deepseek_qwen_14b_s1"  # Vaccination Intent
    version = "vaccine_financial_incentive_vaccinationstatus_llama3.1_8b_s3_updated"  # Vaccination Outcome
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "S3 (LMIC Survey)"  # S1 (Instruct Model), S2 (Instruction-Tuned Model), S3 (LMIC Survey), S4 (LMIC RCT), S5 (LMIC Survey + RCT), S6 (LMIC Pilot), S7 (LMIC Survey + RCT + Pilot)
    model = "Llama 3.1 8B"  # Llama 3.1 8B, Mistral 7B, Mistral 24B, Llama 3.1 70B, Llama 3.3 70B, Claude 3.5 Sonnet, Gemini 1.5 Pro, DeepSeek R1, DeepSeek R1 Distilled Llama 3.3 70B, Deepseek R1 Distilled Qwen 14B
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
    api_url = "https://ic9nt76e9ubp7sap.us-east-1.aws.endpoints.huggingface.cloud/v1/"  # HF dedicated inference endpoint
    model_name = "huggingface"  # huggingface, claude, gemini, together, grok
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
        "backstory_file_path": backstory_file_path,
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
        # Vaccination intent
        # "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
        # "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, and social media use. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video. Thereafter, you will be asked whether you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
        # Vaccination Outcome
        "question": [
            "Have you received a COVID-19 vaccine?",
            "Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?",
        ],
        "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, social media use, and vaccination intention. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video and receive further information on the vaccination intention of your human subject. Thereafter, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    }
    ### Configuration for COVID-19 Vaccination RCT (END) ###

    ### Configuration for TB Screening RCT (START) ###
    # version = "duch_et_al_2025_ghana_tubercolosis_screening_deepseek_llama3.3_70b_s4"
    # current_dir = os.path.dirname(__file__)
    # experiment_round = "round9"
    # scenario = "S4 (LMIC RCT)"  # S1 (Instruct Model), S2 (Instruction-Tuned Model), S3 (LMIC Survey), S4 (LMIC RCT), S5 (LMIC Survey + RCT), S6 (LMIC Pilot), S7 (LMIC Survey + RCT + Pilot)
    # model = "DeepSeek R1 Distilled Llama 3.3 70B"  # Llama 3.1 8B, Mistral 7B, Llama 3.1 70B, Claude 3.5 Sonnet, Gemini 1.5 Pro, Grok 2, DeepSeek R1, DeepSeek R1 Distilled Llama 3.3 70B, Deepseek R1 Distilled Qwen 14B
    # data_file_path = os.path.join(
    #     current_dir,
    #     "../data/duch_et_al_2025_ghana_tubercolosis_screening_training.csv",
    # )
    # backstory_file_path = ""
    # treatment_assignment_column = "treatment"
    # # api_url = (
    # #     "https://router.huggingface.co/together"  # HF serverless inference endpoint
    # # )
    # api_url = "https://fxbuggkyu960a6qw.us-east-1.aws.endpoints.huggingface.cloud/v1/"  # HF dedicated inference endpoint
    # model_name = "huggingface"  # huggingface, claude, gemini, together, grok
    # drop_first_row = True

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "treatment_assignment_column": treatment_assignment_column,
    #     "api_url": api_url,
    #     "model_name": model_name,
    #     "experiment_round": experiment_round,
    #     "demographic_questions": [
    #         "When did this survey start?",
    #         "What is the name of the district you live in?",
    #         "What is the name of the community you live in?",
    #         "How many people live in your community?",
    #         "What is your current age?",
    #         "What is your gender?",
    #         "Which ethnicity best describes you?",
    #         "What is your current working situation?",
    #         "How much on average does your household spend in a typical week on food?",
    #         "How much on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
    #         "How would you rate the overall economic or financial condition of your household today?",
    #         "What is the highest educational qualification you have completed?",
    #         "Do you live with a spouse or partner?",
    #         "Imagine the following situation: Today you unexpectedly received GH‚Çµ 1,610. How much of this amount would you donate to a good cause?",
    #         "How many villages in the district do you think you have visited in the last  month?",
    #         "How many villages in the district do you think you have visited in the last year?",
    #         "How many family members do you have in another village?",
    #         "How many friends and acquaintances who are not part of your family do you have in another village?",
    #         "How many individuals can you identify in your social network? Think of friends and relatives that live close to you",
    #         "How often do you use WhatsApp?",
    #         "What social media have you used in the last year?",
    #         "How often do you use social media?",
    #         "Thinking now about health matters, how familiar are you with tuberculosis? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
    #         "Thinking now about health matters, how familiar are you with high blood pressure/hypertension? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
    #         "Thinking now about health matters, how familiar are you with diabetes? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
    #         "Thinking now about health matters, how familiar are you with asthma? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
    #         "Thinking now about health matters, how familiar are you with heart disease? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
    #         "Which underlying health conditions do you have?",
    #         "How is your health in general?",
    #         "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt cheerful and in good spirits. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
    #         "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt calm and relaxed. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
    #         "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt active and vigorous. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
    #         "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I woke up feeling fresh and rested. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
    #         "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: My daily life has been filled with things that interest me. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
    #         "How much do you trust the following people? - Your relatives",
    #         "How much do you trust the following people? - Your neighbors",
    #         "How much do you trust the following people? - Someone in your own tribe",
    #         "How much do you trust the following people? - Ghanaians from other tribes",
    #         "How much do you trust the following institutions? - Chiefs",
    #         "How much do you trust the following institutions? - District assemblies",
    #         "How much do you trust the following institutions? - The police",
    #         "How much do you trust the following institutions? - Courts of law",
    #         "How much do you trust the following institutions? - Political parties",
    #         "How much do you trust the following institutions? - The army",
    #         "How much do you trust the following institutions? - Parliament",
    #         "How much do you trust the following institutions? - President",
    #         "How much do you trust the following institutions? - Ghana Broadcasting Corporation",
    #         "How much do you trust the following institutions? - Electoral Commission",
    #         "How much do you trust the following non-governmental organizations? - Churches",
    #         "How much do you trust the following non-governmental organizations? - Mosques",
    #         "How much do you trust the following non-governmental organizations? - Trade unions",
    #         "How much do you trust the following non-governmental organizations? - Banks",
    #         "How much do you trust the following non-governmental organizations? - Businesses",
    #         "How is your mobility TODAY?",
    #         "How is your self-care TODAY?",
    #         "How are your usual activities TODAY (e.g. work, study, housework, family or leisure activities)?",
    #         "How is your your pain / discomfort TODAY?",
    #         "How is your anxiety / depression TODAY?",
    #         "How is your health TODAY on a scale from 0 to 100?",
    #         "How many People live in your Household",
    #         "How many children below 18 years old are currently living in your household?",
    #     ],
    #     "question": [
    #         "The Health District Tuberculosis screening team will be in your village within the next two weeks. Would you be willing to get the tuberculosis screening, when the Heath District Tuberculosis screening team is in your village? Please respond with one of these options: Yes, No, Do not know, Prefer not to say.",
    #         "Did you get the tuberculosis screening, when the Heath District Tuberculosis screening team was in your village?",
    #     ],
    #     "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in a remote rural community in Ghana about tuberculosis screening. You will be provided with a demographic profile that describes, among other things, your age, gender, the name and size of your community, your work, your social network, your social media usage, your health, and the people that you trust. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will be provided with the description of an initiative that was carried out in your area and you will watch a video. After you receive your complete human subject profile, you will be asked whether you are willing to get a screening for tuberculosis and whether you received a tuberculosis screening within two weeks from the day of the survey. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # }
    ### Configuration for TB Screening RCT (END) ###

    main(input_data)
