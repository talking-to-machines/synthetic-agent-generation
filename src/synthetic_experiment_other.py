import os
import pandas as pd
from src.data_processing import load_data, include_variable_names
from src.prompt_generation import generate_synthetic_experiment_prompts
from src.api_interaction import inference_endpoint_query


def main(request):
    # Load and preprocess data
    data = load_data(data_file_path, drop_first_row=drop_first_row)

    # Generate demographic prompts
    if request["study"] in ["duch_2023", "duch_2025", "campos"]:
        # ### Configuration for COVID-19 Vaccination RCT, TB Screening RCT, Campos Mercade RCT (START) ###
        prompts = generate_synthetic_experiment_prompts(
            data,
            request["survey_context"],
            request["demographic_questions"],
            request["question"],
            study=request["study"],
        )
        # ### Configuration for COVID-19 Vaccination RCT, TB Screening RCT, Campos Mercade RCT (END) ###

    elif request["study"] in ["milkman_control", "milkman_baseline"]:
        ### Configuration for Milkman et al RCT (START) ###
        if request["study"] == "milkman_control":
            filtered_data = data[data["treatment"].isin(["Control"])].reset_index(
                drop=True
            )  # Control
        else:
            filtered_data = data[
                data["treatment"].isin(["Baseline", "Free ride"])
            ].reset_index(
                drop=True
            )  # Baseline, Free Ride
        prompts = generate_synthetic_experiment_prompts(
            filtered_data,
            request["survey_context"],
            request["demographic_questions"],
            request["question"],
            study=request["study"],
        )
        ### Configuration for Milkman et al RCT (END) ###

    else:
        raise ValueError(f"Study {request['study']} is not supported.")

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

    # For Vaccination Outcome and TB Vaccination
    if request["study"] in ["duch_2023", "duch_2025"]:
        data_with_responses["user_response"] = data_with_responses[
            request["question"][0]
        ]
        data_with_responses["user_response_2"] = data_with_responses[
            request["question"][1]
        ]

    # For Campos Mercade RCT, Milkman RCT
    elif request["study"] in ["campos", "milkman_control", "milkman_baseline"]:
        data_with_responses["user_response"] = data_with_responses[request["question"]]

    else:
        raise ValueError(f"Study {request['study']} is not supported.")

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
    study = "duch_2023"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "S6 (LMIC Pilot)"  # S1 (Instruct Model), S2 (Instruction-Tuned Model), S3 (LMIC Survey), S4 (LMIC RCT), S5 (LMIC Survey + RCT), S6 (LMIC Pilot), S7 (LMIC Survey + RCT + Pilot)
    model = "Llama 3.1 8B"  # Llama 3.1 8B, Mistral 7B, Llama 3.1 70B, Claude 3.5 Sonnet, Gemini 1.5 Pro, Grok 2, DeepSeek R1, DeepSeek R1 Distilled Llama 3.3 70B, Deepseek R1 Distilled Qwen 14B
    api_url = ""  # HF dedicated inference endpoint
    model_name = "together"  # huggingface, claude, gemini, together, grok
    drop_first_row = True
    treatment_assignment_column = "treatment"

    if study == "duch_2023":
        # ### Configuration for COVID-19 Vaccination RCT (START) ###
        version = "vaccine_financial_incentive_vaccinationstatus_llama3.1_8b_wo_intention_s6"  # Vaccination Outcome
        with_intention = True
        holdout_set = True

        if holdout_set:
            data_file_path = os.path.join(
                current_dir,
                "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training_wo_intention_holdout.csv",
            )
        else:
            data_file_path = os.path.join(
                current_dir,
                "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
            )

        input_data = {
            "data_file_path": data_file_path,
            "study": study,
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

    elif study == "duch_2025":
        ### Configuration for TB Screening RCT (START) ###
        version = (
            "duch_et_al_2025_ghana_tubercolosis_screening_deepseek_llama3.3_70b_s4"
        )
        data_file_path = os.path.join(
            current_dir,
            "../data/duch_et_al_2025_ghana_tubercolosis_screening_training.csv",
        )
        input_data = {
            "data_file_path": data_file_path,
            "study": study,
            "treatment_assignment_column": treatment_assignment_column,
            "api_url": api_url,
            "model_name": model_name,
            "experiment_round": experiment_round,
            "demographic_questions": [
                "When did this survey start?",
                "What is the name of the district you live in?",
                "What is the name of the community you live in?",
                "How many people live in your community?",
                "What is your current age?",
                "What is your gender?",
                "Which ethnicity best describes you?",
                "What is your current working situation?",
                "How much on average does your household spend in a typical week on food?",
                "How much on average does your household spend in a typical week on non-food items (electricity, water, rent, school fees)?",
                "How would you rate the overall economic or financial condition of your household today?",
                "What is the highest educational qualification you have completed?",
                "Do you live with a spouse or partner?",
                "Imagine the following situation: Today you unexpectedly received GH‚Çµ 1,610. How much of this amount would you donate to a good cause?",
                "How many villages in the district do you think you have visited in the last  month?",
                "How many villages in the district do you think you have visited in the last year?",
                "How many family members do you have in another village?",
                "How many friends and acquaintances who are not part of your family do you have in another village?",
                "How many individuals can you identify in your social network? Think of friends and relatives that live close to you",
                "How often do you use WhatsApp?",
                "What social media have you used in the last year?",
                "How often do you use social media?",
                "Thinking now about health matters, how familiar are you with tuberculosis? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
                "Thinking now about health matters, how familiar are you with high blood pressure/hypertension? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
                "Thinking now about health matters, how familiar are you with diabetes? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
                "Thinking now about health matters, how familiar are you with asthma? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
                "Thinking now about health matters, how familiar are you with heart disease? Please indicate your familiarity by responding with one of these options: Very High, High, Average, Low, Very Low.",
                "Which underlying health conditions do you have?",
                "How is your health in general?",
                "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt cheerful and in good spirits. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
                "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt calm and relaxed. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
                "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I have felt active and vigorous. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
                "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: I woke up feeling fresh and rested. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
                "Please indicate for the following statement which is closest to how you have been feeling over the last two weeks: My daily life has been filled with things that interest me. Please respond with one of these options: At no time, Some of the time, Less than half of the time, More than half of the time, Most of the time, All the time",
                "How much do you trust the following people? - Your relatives",
                "How much do you trust the following people? - Your neighbors",
                "How much do you trust the following people? - Someone in your own tribe",
                "How much do you trust the following people? - Ghanaians from other tribes",
                "How much do you trust the following institutions? - Chiefs",
                "How much do you trust the following institutions? - District assemblies",
                "How much do you trust the following institutions? - The police",
                "How much do you trust the following institutions? - Courts of law",
                "How much do you trust the following institutions? - Political parties",
                "How much do you trust the following institutions? - The army",
                "How much do you trust the following institutions? - Parliament",
                "How much do you trust the following institutions? - President",
                "How much do you trust the following institutions? - Ghana Broadcasting Corporation",
                "How much do you trust the following institutions? - Electoral Commission",
                "How much do you trust the following non-governmental organizations? - Churches",
                "How much do you trust the following non-governmental organizations? - Mosques",
                "How much do you trust the following non-governmental organizations? - Trade unions",
                "How much do you trust the following non-governmental organizations? - Banks",
                "How much do you trust the following non-governmental organizations? - Businesses",
                "How is your mobility TODAY?",
                "How is your self-care TODAY?",
                "How are your usual activities TODAY (e.g. work, study, housework, family or leisure activities)?",
                "How is your your pain / discomfort TODAY?",
                "How is your anxiety / depression TODAY?",
                "How is your health TODAY on a scale from 0 to 100?",
                "How many People live in your Household",
                "How many children below 18 years old are currently living in your household?",
            ],
            "question": [
                "The Health District Tuberculosis screening team will be in your village within the next two weeks. Would you be willing to get the tuberculosis screening, when the Heath District Tuberculosis screening team is in your village? Please respond with one of these options: Yes, No, Do not know, Prefer not to say.",
                "Did you get the tuberculosis screening, when the Heath District Tuberculosis screening team was in your village?",
            ],
            "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in a remote rural community in Ghana about tuberculosis screening. You will be provided with a demographic profile that describes, among other things, your age, gender, the name and size of your community, your work, your social network, your social media usage, your health, and the people that you trust. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will be provided with the description of an initiative that was carried out in your area and you will watch a video. After you receive your complete human subject profile, you will be asked whether you are willing to get a screening for tuberculosis and whether you received a tuberculosis screening within two weeks from the day of the survey. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
        }
        ### Configuration for TB Screening RCT (END) ###

    elif study == "campos":
        ### Configuration for Campos Mercade RCT (START) ###
        version = "campos_mercade_et_al_2021_monetary_incentives_llama3.1_70b_s7"
        data_file_path = os.path.join(
            current_dir,
            "../data/campos_mercade_et_al_2021_monetary_incentives_increase_COVID_19_vaccinations_training.csv",
        )
        input_data = {
            "data_file_path": data_file_path,
            "study": study,
            "treatment_assignment_column": treatment_assignment_column,
            "api_url": api_url,
            "model_name": model_name,
            "experiment_round": experiment_round,
            "demographic_questions": [
                "In which region do you live?",
                "What year were you born?",
                "Do you identify yourself as a woman or a man?",
                "What describes your civil status best?",
                "What education do you have (fill in the highest you have)?",
                "What is your employment status?",
                "How much in Swedish kronor is your household’s total income per month after taxes including public benefits? Calculate also your loan if you are a student. Please answer even if you are not sure.",
                "Does any child live in your household?",
                "Where was your mother born?",
                "Where was your father born?",
                "How willing are you to give to good causes without expecting anything in return?",
                "In general, how willing are you to take risks?",
                "How willing are you to give up something that is beneficial for you today in order to benefit more from that in the future?",
                "How well do the following statements describe you as a person? When someone does me a favor, I am willing to return it.",
                "How well do the following statements describe you as a person? I assume that people have only the best intentions.",
                "How well do the following statements describe you as a person? I postpone starting on things I dislike to do.",
                "How well do the following statements describe you as a person? It is important for me to always behave properly and to avoid doing anything people would say is wrong.",
                "Have you ever tested positive for COVID-19 or COVID-19 antibodies?",
                "Are you in an at-risk group for COVID-19?",
                "To what extent do you agree with the following statement: In general, COVID-19 vaccines are safe. Please, answer with one of the following options: Completely disagree, Disagree, Neither agree nor disagree, Agree, Completely agree",
                "To what extent do you agree with the following statement: Diseases like autism, multiple sclerosis, and diabetes might be triggered through vaccination. Please, answer with one of the following options: Completely disagree, Disagree, Neither agree nor disagree, Agree, Completely agree",
                "To what extent do you agree with the following statement: I am worried about the side effects from COVID-19 vaccines.  Please, answer with one of the following options: Completely disagree, Disagree, Neither agree nor disagree, Agree, Completely agree",
                "To what extent do you agree with the following statement: I am afraid of the needles used for vaccination. Please, answer with one of the following options: Completely disagree, Disagree, Neither agree nor disagree, Agree, Completely agree",
            ],
            "question": "Have you got a first shot of a COVID-19 vaccine within the first 30 days after the vaccine became available to you? Available means that vaccinations started for people in your age group in your region. Please, answer with one of the following options: Yes, No",
            "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Sweden about the COVID-19 vaccine conducted from May to July 2021. You will be provided with a demographic profile that describes your geographical region, age, gender, civil status, education, employment status, household income, parent’s birthplace, social preferences, and responses to questions related to COVID-19. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will be presented with a text encouraging you to get a COVID-19 vaccine as soon as possible, ideally within the first 30 days after the vaccine becomes available to you. Thereafter, you will be asked some questions about when you think that you will get a first shot of a COVID-19 vaccine and, finally, if you got a first shot of a COVID-19 vaccine within the first 30 days after the vaccine became available to you. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
        }
        ### Configuration for Campos Mercade RCT (END) ###

    elif study in ["milkman_control", "milkman_baseline"]:
        ### Configuration for Milkman et al RCT (START) ###
        if study == "milkman_control":
            version = "milkman_et_al_2024_metastudy_control_llama3.1_70b_s7"  # Control
        else:
            version = "milkman_et_al_2024_metastudy_baseline_freeride_llama3.1_70b_s7"  # Baseline + Free ride

        data_file_path = os.path.join(
            current_dir,
            "../data/Milkman et al - 2024 - megastudy.csv",
        )

        input_data = {
            "data_file_path": data_file_path,
            "study": study,
            "treatment_assignment_column": treatment_assignment_column,
            "api_url": api_url,
            "model_name": model_name,
            "experiment_round": experiment_round,
            "demographic_questions": [
                "What is your gender?",
                "How old were you in October 2022?",
                "What percentage of residents in the ZIP code of your nearest CVS Pharmacy are Hispanic?",
                "What percentage of residents in the ZIP code of your nearest CVS Pharmacy are Black?",
                "What percentage of residents in the ZIP code of your nearest CVS Pharmacy are Asian?",
                "What percentage of residents in the ZIP code of your nearest CVS Pharmacy are White?",
                "What is the median income in the ZIP code of your nearest CVS Pharmacy?",
                "What percentage of residents in the ZIP code of your nearest CVS Pharmacy has a bachelor degree?",
                "What percentage of people in the county of your nearest CVS Pharmacy have completed the primary COVID vaccine series?",
                "What percentage of people in the county of your nearest CVS Pharmacy have completed the primary COVID vaccine series and received at least booster dose?",
                "What percentage of residents in the county of your nearest CVS Pharmacy voted for the Republican candidate?",
                "What is the population density (residents per square mile) in the ZIP code of your nearest CVS Pharmacy?",
                "What is the number of CVS Pharmacies per square mile in the ZIP code of your nearest CVS Pharmacy?",
                "Which medical insurance do you have?",
            ],
        }

        if study == "milkman_control":
            input_data["question"] = (
                "Did you receive a COVID-19 booster shot within 30 days after getting the first message from the CVS Pharmacy?"
            )
            input_data["survey_context"] = (
                "Please put yourself in the shoes of a human subject in the United States in early November 2022. You will be provided with a demographic profile that describes your age, gender, healthcare insurance, and a profile of the ZIP code of your nearest CVS Pharmacy inclusive of population density, median income, percentage of residents with a bachelor degree, percentage of residents with various ethnic backgrounds. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Thereafter, you will be asked if you got a COVID-19 booster by early December 2022, within the first 30 days after the information on your profile was collected. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested."
            )
        else:
            input_data["question"] = (
                "Did you receive a COVID-19 booster shot within 30 days after getting the first message from the CVS Pharmacy?"
            )
            input_data["survey_context"] = (
                "Please put yourself in the shoes of a human subject participating in a healthcare study in the United States about the COVID-19 vaccine carried out in early November 2022. You will be provided with a demographic profile that describes your age, gender, healthcare insurance, and a profile of the ZIP code of your nearest CVS Pharmacy inclusive of population density, median income, percentage of residents with a bachelor degree, percentage of residents with various ethnic backgrounds. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will be presented with a text message encouraging you to get a COVID-19 booster. Thereafter, you will be asked if you got a COVID-19 booster within the first 30 days after receiving the message. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested."
            )
        ### Configuration for Milkman et al RCT (END) ###

    main(input_data)
