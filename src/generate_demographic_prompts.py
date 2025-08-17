import os
import pandas as pd
from src.data_processing import load_data, create_batch_file
from src.prompt_generation import generate_demographic_prompts
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

    # Generate demographic prompts based on different prompt engineering strategies
    prompts = generate_demographic_prompts(
        data,
        request["demographic_questions"],
        system_message=request.get("system_message"),
        question_prompt=request.get("question_prompt"),
    )

    # Perform batch query for creating demographics-primed for each subject
    batch_file_dir = create_batch_file(
        prompts,
        system_message_field="system_message",
        user_message_field="question_prompt",
        batch_file_name=f"batch_input_llm_{scenario}.jsonl",
    )

    batch_query_result = batch_query(
        client,
        batch_input_file_dir=batch_file_dir,
        batch_output_file_dir=f"batch_output_llm_{scenario}.jsonl",
    )

    if scenario == "backstories":
        batch_query_result.rename(columns={"query_response": "backstory"}, inplace=True)

    elif scenario == "interviewsummary":
        batch_query_result.rename(
            columns={"query_response": "interview_summary"}, inplace=True
        )

    elif scenario.startswith("expertreflections"):
        batch_query_result.rename(
            columns={"query_response": "expert_reflection"}, inplace=True
        )  # For expert reflection
        batch_query_result["expert_reflection"] = batch_query_result[
            "expert_reflection"
        ].apply(lambda x: x.replace("\n", " "))

    else:
        raise ValueError("Invalid scenario specified. Please choose a valid scenario.")

    prompts_with_backstory = pd.merge(
        left=prompts, right=batch_query_result, on="custom_id"
    )

    # Save prompts with responses into Excel file
    prompts_with_backstory_file_path = os.path.join(
        current_dir, f"../results/{experiment_round}/{version}.xlsx"
    )
    prompts_with_backstory.to_excel(prompts_with_backstory_file_path, index=False)


if __name__ == "__main__":
    ### Configuration for COVID-19 Vaccination RCT (START) ###
    scenario = "expertreflections_demographer"  # backstories, interviewsummary, expertreflections_psychologist, expertreflections_economist, expertreflections_politicalscientist, expertreflections_demographer
    with_intention = True
    version = f"vaccine_financial_incentive_vaccinationstatus_{scenario}"
    current_dir = os.path.dirname(__file__)
    experiment_round = "round9"
    data_file_path = os.path.join(
        current_dir,
        "../data/duch_et_al_2023_vaccine_financial_vaccination_status_training.csv",
    )
    drop_first_row = True

    input_data = {
        "data_file_path": data_file_path,
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
    }

    if with_intention:
        input_data["demographic_questions"] += [
            "Do you think you will get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you?",
            "Why will you NOT get vaccinated against COVID-19?",
            "We understand that there is always some uncertainty regarding all decisions. From 0% to 100%, what do you think are the chances that you will choose to get a first shot of a COVID-19 vaccine within the first 6 weeks after the vaccine becomes available to you? - 4",
        ]

    if scenario == "backstories":
        input_data.update(
            {
                "system_message": "You are asked to complete some interview questions below\n\n{demographic_info}",
                "question_prompt": "Create your backstory based on the information provided. Please describe in detail in first person narration.",
            }
        )
    elif scenario == "interviewsummary":
        input_data.update(
            {
                "system_message": "Here is a conversation between an interviewer and an interviewee\n\n{demographic_info}",
                "question_prompt": "Succinctly summarize the facts about the interviewee based on the conversation above in a few bullet points in first person narration -- again, think short, concise bullet points",
            }
        )
    elif scenario == "expertreflections_psychologist":
        input_data.update(
            {
                "system_message": "Imagine you are an expert psychologist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
                "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
            }
        )
    elif scenario == "expertreflections_economist":
        input_data.update(
            {
                "system_message": "Imagine you are an expert economist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
                "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
            }
        )
    elif scenario == "expertreflections_politicalscientist":
        input_data.update(
            {
                "system_message": "Imagine you are an expert political scientist (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
                "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
            }
        )
    elif scenario == "expertreflections_demographer":
        input_data.update(
            {
                "system_message": "Imagine you are an expert demographer (with a PhD) taking notes while observing the following interview: \n\n{demographic_info}",
                "question_prompt": "Write observations/reflections about the interviewee. (You should make more than 5 observations and fewer than 20.",
            }
        )
    else:
        raise ValueError("Invalid scenario specified. Please choose a valid scenario.")
    ### Configuration for COVID-19 Vaccination RCT (END) ###

    main(input_data)
