import os
import pandas as pd
from src.data_processing import load_data, create_batch_file, include_variable_names
from src.prompt_generation import (
    generate_synthetic_experiment_prompts,
    generate_replication_experiment_prompts,
    generate_candor_synthetic_experiment_prompts,
)
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
    # cols_of_interest = ["ID"] + request["demographic_questions"] + [request["question"]]
    # cols_of_interest = request["demographic_questions"] + ["ID", request["question"], request["treatment_assignment_column"]]  # TODO synthetic experiments

    # Generate demographic prompts
    ### Configuration for Afrobarometer (START) ###
    # prompts = generate_replication_experiment_prompts(
    #     data,
    #     request["survey_context"],
    #     request["demographic_questions"],
    #     request["question"],
    #     include_backstory=False,  # True if backstory should be included
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
    # data_with_responses["user_response"] = data_with_responses[request["question"][0]]
    # data_with_responses["user_response_2"] = data_with_responses[request["question"][1]]

    # For TB Vaccination
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
    # # version = "afrobarometer_replication_gpt4o_interviewqna"
    # # version = "afrobarometer_replication_gpt4o_interviewsummary"
    # # version = "afrobarometer_replication_gpt4o_interviewqna+backstory"
    # # version = "afrobarometer_replication_gpt4o_interviewqna+expertreflection"
    # version = "afrobarometer_replication_gpt4o_interviewqna+vaccinecontext"
    # # version = "afrobarometer_synthetic_highcash_gpt4.0turbo"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(
    #     current_dir, "../data/afrobarometer_r9_ghana_latlong_training.csv"
    # )
    # backstory_file_path = os.path.join(
    #     current_dir,
    #     "../results/round9/afrobarometer_r9_ghana_latlong_backstory.xlsx",
    #     # current_dir, "../results/round9/afrobarometer_r9_ghana_latlong_expertreflections_combined.xlsx"
    # )
    # drop_first_row = True

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "demographic_questions": [
    #         "Country",
    #         "PSU/EA",
    #         "Region/Province/State",
    #         "Are the following services present in the primary sampling unit/enumeration area: Electricity grid that most houses can access? Answer with No; Yes; Can't determine",
    #         "Are the following services present in the primary sampling unit/enumeration area: Sewage system that most houses can access? Answer with No; Yes; Can't determine",
    #         "Are the following services present in the primary sampling unit/enumeration area: Mobile phone service? Answer with No; Yes; Can't determine",
    #         "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: School (private or public or both)? Answer with No; Yes; Can't determine",
    #         "Are the following facilities present in the primary sampling unit/enumeration area or in easy walking distance: Health clinic (private or public or both)? Answer with No; Yes; Can't determine",
    #         "Date of interview",
    #         "How old are you? Answer with an integer above 17; Refused; Don't know",
    #         "What is the primary language you speak in your home? Answer with Achode; Akan; Atwede; Baasare; Banda; Basare; Bem; Bimoba; Bisa; Bowiri; Brefo; Bulisa; Busanga; Busi; Buuzu; Chamba; Chokosi; Dagaare/Waale; Dagbani; Dagomba; Ekpana; English; Ewe/Anlo; Frafra; Fulani; Ga/Dangbe; Gawo; Gonja; Gruma; Gruni; Grusi; Guan; Hausa; Kabre; Kassem; Konkonba; Kotokoli; Kusaal; Kusasi; Likpakpaln; Mampruli; Moar; Moli; Moshie; Nabt; Nankani; Safalba; Sissali; Taln; Tampulima; Tsala; Wala; Zamrama; Refused; Don't know",
    #         "Let's start with your general view about the current direction of our country. Some people might think the country is going in the wrong direction. Others may feel it is going in the right direction. So let me ask YOU about the overall direction of the country: Would you say that the country is going in the wrong direction or going in the right direction? Answer with Going in the wrong direction; Going in the right direction; Refused; Don't know",
    #         "In general, how would you describe: the present economic condition of this country? Answer with Very bad; Fairly bad; Neither good nor bad; Fairly good; Very good; Refused; Don't know",
    #         "In general, how would you describe: Your own present living conditions? Answer with Very bad; Fairly bad; Neither good nor bad; Fairly good; Very good; Refused; Don't know",
    #         "Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment? Answer with Never; Just once or twice; Several times; Many times; Always; Refused; Don't\nknow",
    #         "When you get together with your friends or family, how often would you say you discuss political matters? Answer with Never; Occasionally; Frequently; Refused; Don't know",
    #         "In this country, how free are you: to choose who to vote for without feeling pressured? Answer with Not at all free; Not very free; Somewhat free; Completely free; Refused; Don't\nknow",
    #         "Let's talk about the last national election held in 2020. People are not always able to vote in elections, for example, because they weren't registered, they were unable to go, or someone prevented them from voting. How about you? In the last national election held in 2020, did you vote, or not, or were you too young to vote? Or can’t you remember whether you voted? Answer with I did not vote; I was too young to vote; I can't remember whether I voted; I voted in the election; Refused; Don't know",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: the [president]? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: [Parliament]? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: your [local government council]? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: the ruling party? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: traditional leaders? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "How much do you trust each of the following, or haven't you heard enough about them to say: religious leaders? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know/Haven't heard enough",
    #         "In the past 12 months have you had contact with a public clinic or hospital? Answer with No; Yes; Refused; Don't know",
    #         "How easy or difficult was it to obtain the medical care or services you needed? Answer with Very easy; Easy; Difficult; Very difficult; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "How often, if ever, did you have to pay a bribe, give a gift, or do a favour for a health worker or clinic or hospital staff in order to get the medical care or services you needed? Answer with Never; Once or twice; A few times; Often; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "In general, when dealing with health workers and clinic or hospital staff, how much do you feel that they treat you with respect? Answer with Not at all; A little bit; Somewhat; A lot; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: lack of medicines or other supplies? Answer with Never; Once or twice; A few times; Often; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: absence of doctors or other medical personnel? Answer with Never; Once or twice; A few times; Often; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: long waiting time? Answer with Never; Once or twice; A few times; Often; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "And have you encountered any of these problems with a public clinic or hospital during the past 12 months: poor condition of facilities? Answer with Never; Once or twice; A few times; Often; Refused; Don't know. Answer No contact if you haven't had any contact with a public clinic or hospital in the past 12 months",
    #         "In your opinion, what are the most important problems facing this country that government should address?",
    #         "Please tell me whether you personally or any other or any other member of your household have been affected in any of the following ways by the COVID-19 pandemic: became ill with, or tested positive for, COVID-19? Answer with Yes; No; Refused; Don't know",
    #         "Please tell me whether you personally or any other or any other member of your household have been affected in any of the following ways by the COVID-19 pandemic: temporarily or permanently lost a job, business, or primary source of income? Answer with Yes; No; Refused; Don't know",
    #         "What is the main reason that you would be unlikely to get a COVID-19 vaccine? Answer with COVID doesn't exist/COVID is not real; Not worried about COVID/COVID is not serious or life-threatening/not deadly; I am at no risk or low risk for getting COVID/Small chance of contracting COVID;\n    I already had COVID and believe I am immune; God will protect me; Don't trust the vaccine/worried about getting fake or counterfeit vaccine;\n    Don't trust the government to ensure the vaccine is safe; Vaccine is not safe; Vaccine was developed too quickly;\n    Vaccine is not effective/Vaccinated people can still get COVID; Vaccine may cause COVID; Vaccine may cause infertility;\n    Vaccine may cause other bad side effects; Vaccines are being used to control or track people; People are being experimented on with vaccines;\n    Afraid of vaccines in general; Allergic to vaccines; Don't like needles;\n    Don't trust the vaccine source/will wait for other vaccines; Effective treatments for COVID are or will be available; It is too difficult to get the vaccine, e.g. have to travel far;\n    Vaccine will be too expensive; I don't know how to get the vaccine; I will wait until others have been vaccinated;\n    I will get the vaccine later; Religious objections to vaccines in general or to the COVID vaccine; Some other reason;\n    Don't know. Answer Not applicable if you've already been vaccinated or have answered you're likely to get vaccinated",
    #         "How much do you trust the government to ensure that any vaccine for COVID-19 that is developed or offered to Ghanaian citizens is safe before it is used in this country? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know",
    #         "How well or badly would you say the current government has managed the response to the COVID-19 pandemic? Answer with Very badly; Fairly badly; Fairly well; Very well; Refused; Don't know",
    #         "When the country is facing a public health emergency like the COVID-19 pandemic, do you agree or disagree that it is justified for the government to temporarily limit democracy or democratic freedoms by taking the following measures: using the police and security forces to enforce public health mandates like restrictions on public gatherings or wearing face masks? Answer with Strongly disagree; Disagree; Neither agree nor disagree; Agree; Strongly agree; Refused; Don't know",
    #         "Now let us talk about the media and how you get information about politics and other issues. How often do you get news from the following sources: radio? Answer with Never; Less than once a month; A few times a month; A few times a week; Every day; Refused; Don't know",
    #         "How often do you get news from the following sources: television? Answer with Never; Less than once a month; A few times a month; A few times a week; Every day; Refused; Don't know",
    #         "How often do you get news from the following sources: print newspapers? Answer with Never; Less than once a month; A few times a month; A few times a week; Every day; Refused; Don't know",
    #         "How often do you get news from the following sources: internet? Answer with Never; Less than once a month; A few times a month; A few times a week; Every day; Refused; Don't know",
    #         "How often do you get news from the following sources: social media such as Facebook, Twitter, WhatsApp, or others? Answer with Never; Less than once a month; A few times a month; A few times a week; Every day; Refused; Don't know",
    #         "Let's go back to talking about you. What is your ethnic community or cultural group? Answer with (National identity) only, or “doesn't think of self in those terms”; Akan; Banda; Basare; Bem; Bisa; Bole; Brefo; Brefo/wala; Bulisa; Busanga; Busi; Buuzu ( mali); Dagaati; Dagbani; Dagomba; Ekpana; Ewe/Anlo; Frafri; Fulani; Ga/Adangbe; Gangaca; Gawo; Gonja; Gruma; Gruni; Grusi; Guan; Gurma; Hausa; Kabre; Kasasi; Kassem; Konkonba; Kotokoli; Kulkulsi; Kusasi; Mamprusi; Mande; Mole-dagbani; Moshie; Nankani; Pampurisi; Safalba; Sissala; Talensi; Taln; Tampluma; Tampulinsi; Templeman; Tsalla; Tsamba; Wale; Wusasi; Zamrama; Zugu; Refused to answer; Don't know",
    #         "Please tell me whether you agree or disagree with the following statement: I feel strong ties with other Ghanaians. Answer with Strongly disagree; Disagree; Neither agree nor disagree; Agree; Strongly agree; Refused; Don't know",
    #         "How much do you trust each of the following types of people: other Ghanaians? Answer with Not at all; Just a little; Somewhat; A lot; Refused; Don't know",
    #         "Do you feel close to any particular political party? Answer with No (does NOT feel close to ANY party); Yes (feels close to a party); Refused to answer; Don't know",
    #         "Which party is that? Answer with BOTH NPP AND NDC; Convention People's Party (CPP); Democratic People's Party (DPP); Don't know; National Democratic Congress (NDC); New Patriotic Party (NPP); Not Applicable; People's National Convention (PNC); Progressive People's Party (PPP); Refused; Refused; Don't know. Answer Not applicable if you don't feel close to any party",
    #         "What is your main occupation? [If unemployed, retired, or disabled, ask:] What was your last main occupation? Answer with Never had a job; Student; Housewife/Homemaker;\n    Agriculture/Farming/Fishing/Forestry; Trader/Hawker/Vendor; Retail/Shop;\n    Unskilled manual worker (e.g. cleaner, laborer, domestic help, unskilled manufacturing worker); Artisan or skilled manual worker (e.g. trades like electrician, mechanic, mechanic, machinist, or skilled manufacturing worker); Clerical or secretarial;\n    Supervisor/Foreman/Senior manager; Security services; Mid-level professional (e.g. teacher, nurse, mid-level government officer);\n    Upper-level professional (e.g. banker/finance, doctor, lawyer, engineer, accountant, professor, senior-level government officer); Other; Refused;\n    Don't know; Retired",
    #         "What is your highest level of education? Answer with No formal schooling; Informal schooling only (including Koranic schooling); Some primary schooling;\n    Primary school completed; Intermediate school or some secondary school/high school; Secondary school/high school completed;\n    Post-secondary qualifications other than university, e.g. a diploma or degree from a polytechnic or college; Some university; University completed;\n    Post-graduate; Refused; Don't know",
    #         "What is your religion, if any? Answer with None; Christian only (i.e., without specific sub-group identification); Roman Catholic; Orthodox; Coptic; Anglican;\n    Lutheran; Methodist; Presbyterian; Baptist; Quaker/Friends; Mennonite;\n    Evangelical; Pentecostal (e.g. “born again” and/or “saved”); Independent (e.g. “African Independent Church”); Jehovah's Witness; Seventh-day Adventist; Mormon;\n    Muslim only (i.e., without specific sub-group identification); Sunni only (i.e., without specific sub-group identification); Ismaeli; Mouridiya Brotherhood; Tijaniya Brotherhood; Qadiriya Brotherhood;\n    Shia; Traditional/Ethnic religion; Hindu; Bahai; Agnostic (Do not know if there is a God); Atheist (Do not believe in a God);\n    Dutch Reformed; Calvinist; Church of Christ; Zionist Christian Church; Jewish; Eglise Du Christianisme Céleste;\n    Fifohazana; Ançardine; Morovian; Faith of Unity; United Church of Zambia or UCZ; New Apostolic Church;\n    Christian mission in many lands (CMML); Salvation Army; Other; Refused; Don't know",
    #         "Respondent's gender Answer with Man; Woman",
    #         "Respondent's race Answer with Black/African; White/European; Coloured/Mixed race; Arab/Lebanese/North African;\n    South Asian (Indian, Pakistani, etc.); East Asian (Chinese, Korean, Indonesian, etc.); Other; Don't know",
    #         "Latitude",
    #         "Longitude",
    #     ],
    #     "question": "Have you received a vaccination against COVID-19, either one or two doses? Answer with No; Yes; Refused; Don't know",
    # Interview Q&A
    # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, and race. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # # Interview Summary
    # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, and race. The information will be provided to you in the format of a short interview summary. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # # Interview + Backstory
    # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, race, and backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # Interview + Expert Reflections
    # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, race, and expert reflections from a psychologist, political scientist, demographer, and economist. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # # Interview + Vaccination Context
    # "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the geographical area/region/district where you live, the facilities and services in your area, your age, view of the country, living conditions, voting preferences, trust in different authorities, experience when seeking healthcare, experience with COVID-19, views on vaccination, preferred sources of information, employment status, highest education level, religion, gender, and race. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # Previous strategy
    # "survey_context":"Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
    # "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, your employment status, the distance to your nearest health clinic, the political party you feel closest to, the percentage vote for the New Patriotic Party in your district, and your backstory. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Additionally, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. Lastly, you will watch a video. After you receive your complete human subject profile, you will be asked about your intentions to receive the COVID-19 vaccine. Assume that you have not been vaccinated against COVID-19. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # }
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

    ### Configuration for COVID-19 Vaccination RCT (START) ###
    # version = "vaccine_financial_incentive_vaccinationintention_gpt4o_chainofthought"  # Vaccination Intent
    # version = "vaccine_financial_incentive_vaccinationstatus_gpt4o_instruct"  # Vaccination Outcome
    # current_dir = os.path.dirname(__file__)
    # experiment_round = "round9"
    # scenario = "instruct"  # instruct, chain_of_thought
    # model = "gpt4o"
    # # data_file_path = os.path.join(
    # #     current_dir,
    # #     "../data/duch_et_al_2023_vaccine_financial_vaccine_intention_training.csv",
    # # )  # Vaccination Intention
    # data_file_path = os.path.join(
    #     current_dir,
    #     "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
    # )  # Vaccination Outcome
    # backstory_file_path = ""
    # treatment_assignment_column = "treatment"
    # drop_first_row = True

    # input_data = {
    #     "data_file_path": data_file_path,
    #     "backstory_file_path": backstory_file_path,
    #     "treatment_assignment_column": treatment_assignment_column,
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
    #         # Only for Vaccination Outcome
    #         "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
    #         "Why will you NOT get vaccinated against COVID-19?",
    #         "We understand that there is always some uncertainty regarding all decisions. From 0% to 100%, what do you think are the chances that you will choose to get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? - 4",
    #     ],
    #     # Vaccination intent
    #     # "question": "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
    #     # "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, and social media use. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video. Thereafter, you will be asked whether you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    #     # Vaccination Outcome
    #     "question": [
    #         "Have you received a COVID-19 vaccine?",
    #         "Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?",
    #     ],
    #     "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana about the COVID-19 vaccine. You will be provided with a demographic profile that describes your age, gender, highest education level you achieved, region/district you live in, size of your village, distance to nearest health clinic in km, household size, current employment situation, average household spending, household economic/financial condition, number of family members and friends in another village, social network, social media use, and vaccination intention. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. Lastly, you will watch a video and receive further information on the vaccination intention of your human subject. Thereafter, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    # }
    ### Configuration for COVID-19 Vaccination RCT (END) ###

    ### Configuration for TB Screening RCT (START) ###
    version = "duch_et_al_2025_ghana_tubercolosis_screening_gpt4o_s1"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    scenario = "S1 (Instruct Model)"  # S1 (Instruct Model)
    model = "GPT 4o"  # GPT 4o
    data_file_path = os.path.join(
        current_dir,
        "../data/duch_et_al_2025_ghana_tubercolosis_screening_training.csv",
    )
    backstory_file_path = ""
    treatment_assignment_column = "treatment"
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
        "backstory_file_path": backstory_file_path,
        "treatment_assignment_column": treatment_assignment_column,
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

    main(input_data)
