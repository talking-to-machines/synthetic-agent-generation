import os
import pandas as pd
from src.data_processing import (
    load_data,
    clean_data,
    create_batch_file
)
from src.prompt_generation import generate_backstory_prompts
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
    data = clean_data(
        data, request["demographic_questions"]
    )

    prompts_with_backstory_all = pd.DataFrame()
    batch_size = len(data)
    for i in tqdm(range(0, len(data), batch_size)):
        batch_data = data[i : i + batch_size].reset_index(drop=True)

        # Generate demographic prompts
        prompts = generate_backstory_prompts(
            batch_data,
            request["demographic_questions"],
        )

        # Perform batch query for creating demographics-primed backstories for each subject
        batch_file_dir = create_batch_file(
            prompts,
            system_message_field="system_message",
            user_message_field="question_prompt",
            batch_file_name="batch_input_llm_backstory.jsonl",
        )

        backstories = batch_query(
            client,
            batch_input_file_dir=batch_file_dir,
            batch_output_file_dir="batch_output_llm_backstory.jsonl",
        )
        backstories.rename(columns={"query_response": "backstory"}, inplace=True)
        backstories["backstory"] = backstories["backstory"].apply(lambda x: x.replace("\n", " "))

        prompts_with_backstory = pd.merge(left=prompts, right=backstories, on="custom_id")
        prompts_with_backstory_all = pd.concat(
            [prompts_with_backstory_all, prompts_with_backstory], ignore_index=True
        )

    # Save prompts with responses into Excel file
    prompts_with_backstory_file_path = os.path.join(
        current_dir, f"../results/round7/{version}.xlsx"
    )
    prompts_with_backstory_all.to_excel(prompts_with_backstory_file_path, index=False)


if __name__ == "__main__":
    ### Configuration for Afrobarometer (START) ###
    # version = "afrobarometer_backstory"
    # current_dir = os.path.dirname(__file__)
    # data_file_path = os.path.join(current_dir, "../data/afrobarometer.xlsx")

    # input_data = {
    #     "data_file_path": data_file_path,
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
    # }
    ### Configuration for Afrobarometer (END) ###

    ### Configuration for CANDOR (START) ###
    version = "candor_backstory_5countries"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/candor_5countries.xlsx")

    input_data = {
        "data_file_path": data_file_path,
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
        ],
    }
    ### Configuration for CANDOR (END) ###

    main(input_data)
