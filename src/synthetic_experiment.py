import os
import pandas as pd
from src.data_processing import (
    load_data,
    clean_data,
    create_batch_file,
)
from src.prompt_generation import generate_synthetic_experiment_prompts, generate_candor_synthetic_experiment_prompts
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
    cols_of_interest = ["ID"] + request["demographic_questions"]
    data = clean_data(
        data, cols_of_interest
    )

    data_with_responses = pd.DataFrame()
    batch_size = len(data)
    for i in tqdm(range(0, len(data), batch_size)):
        batch_data = data.loc[i : i + batch_size, cols_of_interest].reset_index(drop=True)

        # Generate demographic prompts
       ### Configuration for Afrobarometer (START) ###
        # prompts = generate_synthetic_experiment_prompts(
        #     batch_data,
        #     request["survey_context"],
        #     request["demographic_questions"],
        #     request["question"],
        #     include_backstory=True,  # True if backstory should be included
        #     backstory_file_path=request["backstory_file_path"]
        # )
       ### Configuration for Afrobarometer (END) ###

       ### Configuration for CANDOR (START) ###
        prompts = generate_candor_synthetic_experiment_prompts(
            batch_data,
            request["demographic_questions"],
            request["question"],
            include_backstory=True,  # True if backstory should be included
            backstory_file_path=request["backstory_file_path"],
            supplementary_file_path=request["supplementary_file_path"]
        )
       ### Configuration for CANDOR (END) ###

        # Perform batch query for survey questions
        batch_file_dir = create_batch_file(
            prompts,
            system_message_field="system_message",
            user_message_field="question_prompt",
            batch_file_name="batch_input_llm_synthetic_experiment.jsonl",
        )

        llm_responses = batch_query(
            client,
            batch_input_file_dir=batch_file_dir,
            batch_output_file_dir="batch_output_llm_synthetic_experiment.jsonl",
        )

        llm_responses.rename(columns={"query_response": "llm_response"}, inplace=True)

        prompts_with_responses = pd.merge(left=prompts, right=llm_responses, on="custom_id")
        batch_data_with_responses = pd.merge(left=batch_data, right=prompts_with_responses, on="ID")

        data_with_responses = pd.concat(
            [data_with_responses, batch_data_with_responses], ignore_index=True
        )

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/round7/{version}.xlsx"
    )
    data_with_responses.to_excel(prompts_response_file_path, index=False)


if __name__ == "__main__":
    ### Configuration for Afrobarometer (START) ###
    # version = "afrobarometer_synthetic_backstory+cotreasoning_highcash"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/afrobarometer.xlsx")
    # backstory_file_path = os.path.join(current_dir, "../results/round7/afrobarometer_backstory.xlsx")

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
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
    #     "question":"Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",

    #     "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, and the percentage vote for the New Patriotic Party in your district. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. We also provide you with the demographic profile of four other subjects and their responses to several COVID-19 vaccination-related questions in the same survey interview format. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked about your intentions to receive the COVID-19 vaccine. Assume that you have not been vaccinated against COVID-19. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.\n\nHere are four examples of how different subjects have answered the questions. You will see the complete demographic profile of the subject and their answers to the vaccination questions:\nSubject 1 watched a video highlighting that COVID-19 vaccines are being distributed for free by health authorities, emphasizing their safety and effectiveness. After full vaccination, individuals can resume pre-pandemic activities. Additionally, those who receive at least one vaccine shot will be rewarded with 60 Cedi as an incentive to get vaccinated. Subject 1 demographic profile: 1) Interviewer: Do you come from a rural or urban area? Subject 1: Rural 2) Interviewer: How old are you? Subject 1: 46-60 Years Old 3) Interviewer: What is your gender? Subject 1: Woman 4) Interviewer: What is your highest level of education? Subject 1: No formal schooling 5) Interviewer: What is your religion, if any? Subject 1: Anglican 6) Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job? Subject 1: No (not looking) 7) Interviewer: What region do you come from? Subject 1: NORTHERN 8) Interviewer: Do you feel close to any particular political party? Subject 1: Does not know 9) Interviewer: When you get together with your friends or family, how often would you say you discuss political matters? Subject 1: Never 10) Interviewer: Latitude Subject 1: 9.67748775 11) Interviewer: Longitude Subject 1: -2.7059049 12) Interviewer: What is the distance to the nearest health clinic from your location in kilometers? Subject 1: 0.675554777 13) Interviewer: What district do you live in? Subject 1: WaWest 14) Interviewer: What percentage of the population in your district voted for the National Democratic Congress (NDC)? Subject 1: 67.4290964 15) Interviewer: What percentage of the population in your district voted for the New Patriotic Party (NPP)? Subject 1: 24.6669407 16) Interviewer: In the past 12 months, have you had contact with a public clinic or hospital? Subject 1: No 17) Have you received a vaccination against COVID-19, either one or two doses? Subject 1: No 18) Interviewer: Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? Subject 1: No\nSubject 2 watched a video highlighting that COVID-19 vaccines are being distributed for free by health authorities, emphasizing their safety and effectiveness. After full vaccination, individuals can resume pre-pandemic activities. Additionally, those who receive at least one vaccine shot will be rewarded with 60 Cedi as an incentive to get vaccinated. Subject 2 demographic profile: 1) Interviewer: Do you come from a rural or urban area? Subject 2: Urban 2) Interviewer: How old are you? Subject 2: > 60 Years Old 3) Interviewer: What is your gender? Subject 2: Man 4) Interviewer: What is your highest level of education? Subject 2: Primary school completed 5) Interviewer: What is your religion, if any? Subject 2: Orthodox 6) Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job? Subject 2: Yes, full time 7) Interviewer: What region do you come from? Subject 2: EASTERN 8) Interviewer: Do you feel close to any particular political party? Subject 2: Yes (feels close to a party) 9) Interviewer: When you get together with your friends or family, how often would you say you discuss political matters? Subject 2: Frequently 10) Interviewer: Latitude Subject 2: 5.982346250000001 11) Interviewer: Longitude Subject 2: 0.4963226166666666 12) Interviewer: What is the distance to the nearest health clinic from your location in kilometers? Subject 2: 3.306559877 13) Interviewer: What district do you live in? Subject 2: AdaWest 14) Interviewer: What percentage of the population in your district voted for the National Democratic Congress (NDC)? Subject 2: 69.9223417 15) Interviewer: What percentage of the population in your district voted for the New Patriotic Party (NPP)? Subject 2: 24.516129 16) Interviewer: In the past 12 months, have you had contact with a public clinic or hospital? Subject 2: Yes 17) Have you received a vaccination against COVID-19, either one or two doses? Subject 2: No 18) Interviewer: Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? Subject 2: Yes\nSubject 3 watched a video highlighting that COVID-19 vaccines are being distributed for free by health authorities, emphasizing their safety and effectiveness. After full vaccination, individuals can resume pre-pandemic activities. Additionally, those who receive at least one vaccine shot will be rewarded with 60 Cedi as an incentive to get vaccinated. Subject 3 demographic profile: 1) Interviewer: Do you come from a rural or urban area? Subject 3: Urban 2) Interviewer: How old are you? Subject 3: 18-30 Years Old 3) Interviewer: What is your gender? Subject 3: Woman 4) Interviewer: What is your highest level of education? Subject 3: Intermediate school or Some secondary school / high school 5) Interviewer: What is your religion, if any? Subject 3: Christian only (i.e., respondents says only 'Christian', without identifying a specific sub-group) 6) Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job? Subject 3: No (not looking) 7) Interviewer: What region do you come from? Subject 3: CENTRAL 8) Interviewer: Do you feel close to any particular political party? Subject 3: No (does NOT feel close to ANY party) 9) Interviewer: When you get together with your friends or family, how often would you say you discuss political matters? Subject 3: Occasionally 10) Interviewer: Latitude Subject 3: 5.814093683333335 11) Interviewer: Longitude Subject 3: -0.18634315 12) Interviewer: What is the distance to the nearest health clinic from your location in kilometers? Subject 3: 0.009500653 13) Interviewer: What district do you live in? Subject 3: AkwapemSouth 14) Interviewer: What percentage of the population in your district voted for the National Democratic Congress (NDC)? Subject 3: 30.6572442 15) Interviewer: What percentage of the population in your district voted for the New Patriotic Party (NPP)? Subject 3: 66.3310182 16) Interviewer: In the past 12 months, have you had contact with a public clinic or hospital? Subject 3: No 17) Have you received a vaccination against COVID-19, either one or two doses? Subject 3: No 18) Interviewer: Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? Subject 3: Yes\nSubject 4 watched a video highlighting that COVID-19 vaccines are being distributed for free by health authorities, emphasizing their safety and effectiveness. After full vaccination, individuals can resume pre-pandemic activities. Additionally, those who receive at least one vaccine shot will be rewarded with 60 Cedi as an incentive to get vaccinated. Subject 4 demographic profile: 1) Interviewer: Do you come from a rural or urban area? Subject 4: Rural 2) Interviewer: How old are you? Subject 4: 18-30 Years Old 3) Interviewer: What is your gender? Subject 4: Man 4) Interviewer: What is your highest level of education? Subject 4: Some university 5) Interviewer: What is your religion, if any? Subject 4: Jehovah's Witness 6) Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job? Subject 4: No (looking) 7) Interviewer: What region do you come from? Subject 4: WESTERN 8) Interviewer: Do you feel close to any particular political party? Subject 4: Refused to answer 9) Interviewer: When you get together with your friends or family, how often would you say you discuss political matters? Subject 4: Never 10) Interviewer: Latitude Subject 4: 6.729344933333334 11) Interviewer: Longitude Subject 4: -1.64168995 12) Interviewer: What is the distance to the nearest health clinic from your location in kilometers? Subject 4: 0.515928711 13) Interviewer: What district do you live in? Subject 4: Suame 14) Interviewer: What percentage of the population in your district voted for the National Democratic Congress (NDC)? Subject 4: 15.8331544 15) Interviewer: What percentage of the population in your district voted for the New Patriotic Party (NPP)? Subject 4: 83.0350037 16) Interviewer: In the past 12 months, have you had contact with a public clinic or hospital? Subject 4: No 17) Have you received a vaccination against COVID-19, either one or two doses? Subject 4: No 18) Interviewer: Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? Subject 4: Yes"
    # }
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    version = "candor_synthetic_backstory+cotreasoning_placebo_13084"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/candor_13084.xlsx")
    backstory_file_path = os.path.join(current_dir, "../results/round7/candor_backstory_5countries.xlsx")
    supplementary_file_path = os.path.join(current_dir, "../results/round7/candor_supplementary.xlsx")

    input_data = {
        "data_file_path": data_file_path,
        "backstory_file_path": backstory_file_path,
        "supplementary_file_path":supplementary_file_path,
        "demographic_questions": [
            'What is your gender?', 
            'What is your age?',
            "The following is a scale from 0 to 10 that goes from left to right, where 0 means 'Left' and 10 means 'Right'. Today when talking about political trends, many people talk about those who are more sympathetic to the left or the right. According to the sense that the terms 'Left' and 'Right' have for you when you think about your political point of view, where would you find yourself on this scale?",
            'Gross HOUSEHOLD income combines your gross income with that of your partner or any other household member with whom you share financial responsibilities BEFORE any taxes are paid and BEFORE any benefits are obtained. What is your gross annual household income?',
            'Thinking back to 12 months ago, has your household income increased or decreased since then?',
            'We would like to know how good or bad your health is TODAY. How would you rate your health today on a scale numbered 0 to 100? 100 means the best health you can imagine. 0 means the worst health you can imagine.',
            'What is the highest degree or level of education you have completed?',
            'Do you have any dependent children who live with you? (By "dependent" children, we mean those who are not yet financially independent).',
            'Are you currently married, in a civil partnership, or living with a partner?',
            'Would you vote to re-elect this government in the next election?',
            'Overall, how would you rate the current government on a scale of 0 (very low rating) to 100 (very high rating)?',
            'Where in the country do you live?',
            'country'
        ],
        "question":"Since you watched this video six weeks ago, do you think you will get a first shot of a COVID-19 vaccine if the vaccine becomes available to you?",

        "survey_context":""
    }
    ### Configuration for CANDOR (END) ###

    main(input_data)
