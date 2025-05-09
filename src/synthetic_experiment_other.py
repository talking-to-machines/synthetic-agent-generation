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

    # Generate demographic prompts
    ### Configuration for Afrobarometer Ghana (START) ###
    # prompts = generate_replication_experiment_prompts(
    #     data,
    #     request["survey_context"],
    #     request["demographic_questions"],
    #     request["question"],
    #     include_backstory=True,  # True if backstory should be included
    #     backstory_file_path=request["backstory_file_path"],
    # )
    ### Configuration for Afrobarometer Ghana (END) ###

    ### Configuration for COVID-19 Vaccination RCT and TB Screening RCT (START) ###
    prompts = generate_replication_experiment_prompts(
        data,
        request["survey_context"],
        request["demographic_questions"],
        request["question"],
        include_backstory=False,  # True if backstory should be included
        backstory_file_path=request["backstory_file_path"],
    )
    ### Configuration for COVID-19 Vaccination RCT and TB Screening RCT (END) ###

    ### Configuration for COVID-19 Vaccination RCT and TB Screening RCT (START) ###
    # prompts = generate_synthetic_experiment_prompts(
    #     data,
    #     request["survey_context"],
    #     request["demographic_questions"],
    #     request["question"],
    #     include_backstory=False,  # True if backstory should be included
    #     backstory_file_path=request["backstory_file_path"],
    # )
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

    # For Vaccination Outcome and TB Vaccination and Afrobarometer Nigeria
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
    ### Configuration for Afrobarometer Ghana (START) ###
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
    ### Configuration for Afrobarometer Ghana (END) ###

    ### Configuration for Afrobarometer Nigeria (START) ###
    version = "afrobarometer_nigeria_robustness_analysis_llama3.1_8b_s3"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "S3 (LMIC Survey)"  # S1 (Instruct Model), S2 (Instruction-Tuned Model), S3 (LMIC Survey), S4 (LMIC RCT), S5 (LMIC Survey + RCT), S6 (LMIC Pilot), S7 (LMIC Survey + RCT + Pilot)
    model = "Llama 3.1 8B"  # Llama 3.1 8B, Mistral 7B, Llama 3.1 70B, Claude 3.5 Sonnet, Gemini 1.5 Pro, Grok 2, DeepSeek R1, DeepSeek R1 Distilled Llama 3.3 70B, Deepseek R1 Distilled Qwen 14B
    data_file_path = os.path.join(
        current_dir,
        "../data/afrobarometer_NIGERIA_training.csv",
    )  # Vaccination Outcome
    backstory_file_path = ""
    treatment_assignment_column = "treatment"
    api_url = "https://qiw92sl4ihshdvnd.us-east-1.aws.endpoints.huggingface.cloud/v1/"  # HF dedicated inference endpoint
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
            "Respondent Number",
            "Country",
            "PSU/EA",
            "Region/Province/State",
            "Are the following services present in the primary sampling unit/enumeration area: Electricity grid that most houses can access?",
            "Are the following services present in the primary sampling unit/enumeration area: Piped water system that most houses can access?",
            "Are the following services present in the primary sampling unit/enumeration area: Sewage system that most houses can access?",
            "Are the following services present in the primary sampling unit/enumeration area: Mobile phone service?",
            "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: School (private or public or both)?",
            "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: Health clinic (private or public or both)?",
            "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: A social center, government help center, or other government office where people can request help with problems?",
            "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: Is there any kind of paid transport, such as a bus, taxi, moped, or other form, available on a daily basis?",
            "Date of interview",
            "How old are you?",
            "What is the primary language you speak in your home?",
            "Let's start with your general view about the current direction of our country. Some people might think the country is going in the wrong direction. Others may feel it is going in the right direction. So let me ask YOU about the overall direction of the country: Would you say that the country is going in the wrong direction or going in the right direction?",
            "In general, how would you describe: the present economic condition of this country?",
            "In general, how would you describe: Your own present living conditions?",
            "Looking back, how do you rate economic conditions in this country compared to 12 months ago?",
            "Looking ahead, do you expect economic conditions in this country to be better or worse in 12 months' time?",
            "Over the past year, how often, if ever, have you or anyone in your family gone without: Enough food to eat?",
            "Over the past year, how often, if ever, have you or anyone in your family gone without: Enough clean water for home use?",
            "Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment?",
            "Over the past year, how often, if ever, have you or anyone in your family gone without: Enough fuel to cook your food?",
            "Over the past year, how often, if ever, have you or anyone in your family gone without: A cash income?",
            "When you get together with your friends or family, how often would you say you discuss political matters?",
            "In this country, how free are you: to say what you think?",
            "In this country, how free are you: to join any political organization you want?",
            "In this country, how free are you: to choose who to vote for without feeling pressured?",
            "Let's talk about the last national election held in 2019. People are not always able to vote in elections, for example, because they weren't registered, they were unable to go, or someone prevented them from voting. How about you? In the last national election held in 2019, did you vote, or not, or were you too young to vote? Or can’t you remember whether you voted?",
            "Which of the following statements is closest to your view? Choose Statement 1 or Statement 2. Statement 1: It is more important to have a government that can get things done, even if we have no influence over what it does. Statement 2: It is more important for citizens to be able to hold government accountable, even if that means it makes decisions more slowly.",
            "Which of the following statements is closest to your view? Choose Statement 1 or Statement 2. Statement 1: The government is like the people's boss. People should respect the government and do what it directs. Statement 2: The government is like the people's employee. It should respect the citizens and do what they request.",
            "How much do you trust each of the following, or haven't you heard enough about them to say: the [president]?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: [Parliament]?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: your [local government council]?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: the ruling party?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: opposition political parties?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: traditional leaders?",
            "How much do you trust each of the following, or haven't you heard enough about them to say: religious leaders?",
            "In the past 12 months have you had contact with a public clinic or hospital?",
            "How easy or difficult was it to obtain the medical care or services you needed?",
            "How often, if ever, did you have to pay a bribe, give a gift, or do a favour for a health worker or clinic or hospital staff in order to get the medical care or services you needed?",
            "In general, when dealing with health workers and clinic or hospital staff, how much do you feel that they treat you with respect?",
            "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: lack of medicines or other supplies?",
            "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: absence of doctors or other medical personnel?",
            "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: long waiting time?",
            "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: poor condition of facilities?",
            "In your opinion, what are the most important problems facing this country that government should address?",
            "For each of the following statements, please tell me whether you agree or disagree: in my community, children and adults who have mental or emotional problems are generally able to get the help they need to have a good life.",
            "Please tell me whether you personally or any other or any other member of your household have been affected in any of the following ways by the COVID-19 pandemic: became ill with, or tested positive for, COVID-19?",
            "Please tell me whether you personally or any other or any other member of your household have been affected in any of the following ways by the COVID-19 pandemic: temporarily or permanently lost a job, business, or primary source of income?",
            "What is the main reason that you would be unlikely to get a COVID-19 vaccine?",
            "How much do you trust the government to ensure that any vaccine for COVID-19 that is developed or offered to Nigerian citizens is safe before it is used in this country?",
            "How well or badly would you say the current government has managed the response to the COVID-19 pandemic?",
            "How satisfied or dissatisfied are you with the government's response to COVID-19 in the following areas: providing relief to vulnerable households?",
            "How satisfied or dissatisfied are you with the government's response to COVID-19 in the following areas: ensuring that disruptions to children's education are kept to a minimum?",
            "How satisfied or dissatisfied are you with the government's response to COVID-19 in the following areas: making sure that health facilities have adequate resources to respond to the COVID-19 pandemic?",
            "Considering all of the funds and resources that were available to the government for combating and responding to the COVID-19 pandemic, how much do you think was lost or stolen due to corruption?",
            "When the country is facing a public health emergency like the COVID-19 pandemic, do you agree or disagree that it is justified for the government to temporarily limit democracy or democratic freedoms by taking the following measures: censoring media reporting?",
            "When the country is facing a public health emergency like the COVID-19 pandemic, do you agree or disagree that it is justified for the government to temporarily limit democracy or democratic freedoms by taking the following measures: using the police and security forces to enforce public health mandates like restrictions on public gatherings or wearing face masks?",
            "When the country is facing a public health emergency like the COVID-19 pandemic, do you agree or disagree that it is justified for the government to temporarily limit democracy or democratic freedoms by taking the following measures: postponing elections?",
            "After experiencing the COVID-19 pandemic in Nigeria, how prepared or unprepared do you think the government will be to deal with future public health emergencies?",
            "Do you agree or disagree wit the following statement: our government needs to invest more of our health resources in special preparations to respond to health emergencies like COVID-19, even if it means fewer resources are available for other health services?",
            "Since the start of the COVID-19 pandemic, have you or your household received any assistance from government, like food, cash payments, relief from bill payments, or other assistance that you were not normally receiving before the pandemic?",
            "Do you think that the distribution of government support to people during the COVID-19 pandemic, for example through food packages or cash payments, has been fair or unfair?",
            "Now let us talk about the media and how you get information about politics and other issues. How often do you get news from the following sources: radio?",
            "How often do you get news from the following sources: television?",
            "How often do you get news from the following sources: print newspapers?",
            "How often do you get news from the following sources: internet?",
            "How often do you get news from the following sources: social media such as Facebook, Twitter, WhatsApp, or others?",
            "Do you agree or disagree with the following statement: information held by public authorities is only for use by government officials; it should not have to be shared with the public.",
            "What is your ethnic community or cultural group?",
            "Please tell me whether you agree or disagree with the following statement: I feel strong ties with other Nigerians.",
            "How much do you trust each of the following types of people: other Nigerians?",
            "How much do you trust each of the following types of people: your relatives?",
            "How much do you trust each of the following types of people: your neighbours?",
            "How much do you trust each of the following types of people: other people you know?",
            "Do you feel close to any particular political party?",
            "Which party is that?",
            "Do you personally own a mobile phone or does anyone in your household own one?",
            "Does your phone have access to the internet?",
            "How often do you use: a mobile phone?",
            "How often do you use: the Internet?",
            "What is your main occupation? [If unemployed, retired, or disabled, ask:] What was your last main occupation?",
            "What is your highest level of education?",
            "What is your religion, if any?",
            "Respondent's gender",
            "Respondent's race",
        ],
        "question": [
            "Have you received a vaccination against COVID-19, either one or two doses? Answer with No; Yes; Refused; Don't know",
            "If a vaccine for COVID-19 is available, how likely are you to try to get vaccinated? Answer with Very unlikely; Somewhat unlikely; Somewhat likely; Very likely; Refused; Don't know. Answer Not applicable if you have already received a COVID-19 vaccination",
        ],
        "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Nigeria. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, and race. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    }
    ### Configuration for Afrobarometer Nigera (END) ###

    # ### Configuration for COVID-19 Vaccination RCT (START) ###
    # version = "vaccine_financial_incentive_vaccinationstatus_deepseek_qwen_14b_s4"  # Vaccination Outcome
    # current_dir = os.path.dirname(__file__)
    # experiment_round = "round9"
    # scenario = "S4 (LMIC RCT)"  # S1 (Instruct Model), S2 (Instruction-Tuned Model), S3 (LMIC Survey), S4 (LMIC RCT), S5 (LMIC Survey + RCT), S6 (LMIC Pilot), S7 (LMIC Survey + RCT + Pilot)
    # model = "Deepseek R1 Distilled Qwen 14B"  # Llama 3.1 8B, Mistral 7B, Llama 3.1 70B, Claude 3.5 Sonnet, Gemini 1.5 Pro, Grok 2, DeepSeek R1, DeepSeek R1 Distilled Llama 3.3 70B, Deepseek R1 Distilled Qwen 14B
    # data_file_path = os.path.join(
    #     current_dir,
    #     "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
    # )  # Vaccination Outcome
    # backstory_file_path = ""
    # treatment_assignment_column = "treatment"
    # api_url = "https://dh0lok4am4vzumvg.us-east-1.aws.endpoints.huggingface.cloud/v1/"  # HF dedicated inference endpoint
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
    #         "Start Date",
    #         "What is your current age?",
    #         "What is your gender?",
    #         "What is the highest educational qualification you have completed?",
    #         "Which region do you live in?",
    #         "Which distric do you live in?",
    #         "What is the name of the community you live in?",
    #         "How many people live in your village?",
    #         "What is the distance in km of the nearest health clinic from where you live?",
    #         "How many people live in the house together with you (NOT including you) at this moment?",
    #         "How many children below 18 years old are currently living in your home?",
    #         "What is your current working situation?",
    #         "How much (in Ghanaian Cedis) on average does your household spend in a typical week on food?",
    #         "How much (in Ghanaian Cedis) on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
    #         "How would you rate the overall economic or financial condition of your household today?",
    #         "Do you have a registered mobile number?",
    #         "How many family members do you have in another village?",
    #         "How many friends and acquaintances who are not part of your family do you have in another village?",
    #         "How many individuals can you identify in your social network? Think of friends and relatives that live close to you",
    #         "How often do you use social media?",
    #         # TODO REMOVE
    #         "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
    #         "Why will you NOT get vaccinated against COVID-19?",
    #         "We understand that there is always some uncertainty regarding all decisions. From 0% to 100%, what do you think are the chances that you will choose to get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? - 4",
    #         # TODO REMOVE
    #     ],
    #     "question": [
    #         "Have you received a COVID-19 vaccine?",
    #         "Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?",
    #     ],
    #     "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, social media use, and vaccination intention. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video and receive further information on the vaccination intention of your human subject. Thereafter, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # }
    # ### Configuration for COVID-19 Vaccination RCT (END) ###

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
