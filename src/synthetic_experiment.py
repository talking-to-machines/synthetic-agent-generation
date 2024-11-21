import os
import pandas as pd
from src.data_processing import (
    load_data,
    clean_data,
    create_batch_file,
)
from src.prompt_generation import (
    generate_synthetic_experiment_prompts,
    generate_replication_experiment_prompts,
    generate_candor_synthetic_experiment_prompts,
)
from src.api_interaction import batch_query
from openai import OpenAI
from config.settings import OPENAI_API_KEY
from tqdm import tqdm


def main(request):
    # Load OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    # Load and preprocess data
    data = load_data(data_file_path)
    ### Configuration for Afrobarometer (START) ###
    # cols_of_interest = ["ID"] + request["demographic_questions"] + [request["question"]]
    cols_of_interest = ["ID"] + request["demographic_questions"]
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for Ghana Wave I/II (START) ###
    # cols_of_interest = ["ID"] + request["demographic_questions"] + ["Treatment", request["question"]]
    ### Configuration for Ghana Wave I/II (END) ###

    # data = clean_data(data, cols_of_interest)

    data_with_responses = pd.DataFrame()
    batch_size = len(data)
    for i in tqdm(range(0, len(data), batch_size)):
        batch_data = data.loc[i : i + batch_size, cols_of_interest].reset_index(
            drop=True
        )

        # Generate demographic prompts
        ### Configuration for Afrobarometer (START) ###
        prompts = generate_replication_experiment_prompts(
            batch_data,
            request["survey_context"],
            request["demographic_questions"],
            request["question"],
            include_backstory=True,  # True if backstory should be included
            backstory_file_path=request["backstory_file_path"],
        )
        ### Configuration for Afrobarometer (END) ###

        ### Configuration for CANDOR (START) ###
        # prompts = generate_candor_synthetic_experiment_prompts(
        #     batch_data,
        #     request["demographic_questions"],
        #     request["question"],
        #     include_backstory=True,  # True if backstory should be included
        #     backstory_file_path=request["backstory_file_path"],
        #     supplementary_file_path=request["supplementary_file_path"]
        # )
        ### Configuration for CANDOR (END) ###

        ### Configuration for Ghana Wave I/II (START) ###
        # prompts = generate_synthetic_experiment_prompts(
        #     batch_data,
        #     request["survey_context"],
        #     request["demographic_questions"],
        #     request["question"],
        #     include_backstory=True,  # True if backstory should be included
        #     backstory_file_path=request["backstory_file_path"]
        # )
        ### Configuration for Ghana Wave I/II (END) ###

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

        prompts_with_responses = pd.merge(
            left=prompts, right=llm_responses, on="custom_id"
        )
        batch_data_with_responses = pd.merge(
            left=batch_data, right=prompts_with_responses, on="ID"
        )

        data_with_responses = pd.concat(
            [data_with_responses, batch_data_with_responses], ignore_index=True
        )

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/round8/{version}.xlsx"
    )
    data_with_responses.to_excel(prompts_response_file_path, index=False)


if __name__ == "__main__":
    ### Configuration for Afrobarometer (START) ###
    # version = "afrobarometer_replication_gpt4o"
    version = "afrobarometer_synthetic_highcash_gpt4.0turbo"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/afrobarometer.xlsx")
    backstory_file_path = os.path.join(
        current_dir, "../results/round8/afrobarometer_backstory.xlsx"
    )

    input_data = {
        "data_file_path": data_file_path,
        "backstory_file_path": backstory_file_path,
        "demographic_questions": [
            "Do you come from a rural or urban area?",
            "How old are you?",
            "What is your gender?",
            "What is your highest level of education?",
            "What is your religion, if any?",
            "Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job?",
            "What region do you come from?",
            "Do you feel close to any particular political party?",
            "When you get together with your friends or family, how often would you say you discuss political matters?",
            "Latitude",
            "Longitude",
            "What is the distance to the nearest health clinic from your location in kilometers?",
            "What district do you live in?",
            "What percentage of the population in your district voted for the National Democratic Congress (NDC)?",
            "What percentage of the population in your district voted for the New Patriotic Party (NPP)?",
            "In the past 12 months, have you had contact with a public clinic or hospital?",
        ],
        # "question":"Have you received a vaccination against COVID-19, either one or two doses?",
        # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
        "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
        "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked about your intentions to receive the COVID-19 vaccine. Assume that you have not been vaccinated against COVID-19. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    }
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    # version = "candor_synthetic_backstory+cotreasoning_highcash_sample_600"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/candor_sample_600.xlsx")
    # backstory_file_path = os.path.join(current_dir, "../results/round7/candor_backstory_5countries.xlsx")
    # supplementary_file_path = os.path.join(current_dir, "../results/round7/candor_supplementary.xlsx")

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

    ### Configuration for Ghana Wave I (START) ###
    # version = "ghana_wave_1_synthetic_vaccineintent_gpt4.0turbo"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/ghana_wave_1.csv")
    # backstory_file_path = os.path.join(current_dir, "../results/round8/ghana_wave_1_backstory.xlsx")

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "demographic_questions": [
    #         "What is your current age?",
    #         "What is your gender?",
    #         "How many people live in the house together with you (NOT including you) at this moment?",
    #         "How many children below 18 years old are currently living in your home?",
    #         "What is your current working situation?",
    #         "How much on average does your household spend in a typical week on food?",
    #         "How much on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
    #         "How would you rate the overall economic or financial condition of your household today?",
    #         "What is the highest educational qualification you have completed?",
    #         "How many villages in the district do you think you have visited in the last month?",
    #         "How many villages in the district do you think you have visited in the last year?",
    #         "Do you have family in other villages in the district?",
    #         "Do you have WhatsApp?",
    #         "How often do you use WhatsApp?",
    #         "What social media have you used in the last year? - Facebook",
    #         "What social media have you used in the last year? - Twitter",
    #         "What social media have you used in the last year? - Instagram",
    #         "What social media have you used in the last year? - Reddit",
    #         "What social media have you used in the last year? - YouTube",
    #         "What social media have you used in the last year? - SnapChat",
    #         "What social media have you used in the last year? - TikTok",
    #         "What social media have you used in the last year? - Other",
    #         "What social media have you used in the last year? - I don't use social media",
    #         "How often do you use social media?",
    #         "Distance to clinic in km"
    #     ],
    #     "question":"Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",

    #     "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes your gender, the highest education level you achieved, your household size, your employment status, your financial situation, the number of villages you visited, your usage of WhatsApp and other social media, the distance to your nearest health clinic, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested."
    # }
    ### Configuration for Ghana Wave I (END) ###

    ### Configuration for Ghana Wave II (START) ###
    # version = "ghana_wave_2_synthetic_vaccineintent_gpt4.0turbo"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/ghana_wave_2.csv")
    # backstory_file_path = os.path.join(current_dir, "../results/round8/ghana_wave_2_backstory.xlsx")

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "demographic_questions": [
    #         "What is your current age?",
    #         "What is your gender?",
    #         "What is your current working situation?",
    #         "How much on average does your household spend in a typical week on food?",
    #         "How much on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
    #         "How would you rate the overall economic or financial condition of your household today?",
    #         "What is the highest educational qualification you have completed?",
    #         "How many villages in the district do you think you have visited in the last month?",
    #         "How many villages in the district do you think you have visited in the last year?",
    #         "Do you have family in other villages in the district?",
    #         "Do you have WhatsApp?",
    #         "How often do you use WhatsApp?",
    #         "What social media have you used in the last year? - Facebook",
    #         "What social media have you used in the last year? - Twitter",
    #         "What social media have you used in the last year? - Instagram",
    #         "What social media have you used in the last year? - Reddit",
    #         "What social media have you used in the last year? - YouTube",
    #         "What social media have you used in the last year? - SnapChat",
    #         "What social media have you used in the last year? - TikTok",
    #         "What social media have you used in the last year? - Other",
    #         "What social media have you used in the last year? - I don't use social media",
    #         "How often do you use social media?",
    #         "How many people live in your household?",
    #         "How many children below 18 years old are currently living in your household?",
    #     ],
    #     "question":"The Health District Tuberculosis screening team will be in your village within the next two weeks. Would you be willing to get the tuberculosis screening, when the Heath District Tuberculosis screening team is in your village?",

    #     "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes your gender, the highest education level you achieved, your household size, your employment status, your financial situation, the number of villages you visited, your usage of WhatsApp and other social media, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked whether you are willing to get a screening for Tuberculosis. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested."
    # }
    ### Configuration for Ghana Wave II (END) ###

    main(input_data)
