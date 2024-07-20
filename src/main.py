import os
import pandas as pd
from src.data_processing import (
    load_data,
    clean_data,
    merge_prompts_with_responses,
    create_batch_file,
)
from src.prompt_generation import generate_prompts
from src.api_interaction import batch_query
from src.evaluation import evaluate_responses
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
        data, request["demographic_questions"] + request["survey_questions"]
    )

    prompts_with_responses_all = pd.DataFrame()
    batch_size = 200
    for i in tqdm(range(0, len(data), batch_size)):
        batch_data = data[i : i + batch_size].reset_index(drop=True)

        # Generate demographic prompts
        prompts = generate_prompts(
            client,
            batch_data,
            request["survey_context"],
            request["demographic_questions"],
            request["survey_questions"],
        )

        # Perform batch query for survey questions
        batch_file_dir = create_batch_file(
            prompts,
            system_message_field="system_message",
            user_message_field="question_prompt",
            batch_file_name="batch_input_llm_survey_response.jsonl",
        )

        llm_responses = batch_query(
            client,
            batch_input_file_dir=batch_file_dir,
            batch_output_file_dir="batch_output_llm_survey_response.jsonl",
        )
        llm_responses.rename(columns={"query_response": "llm_response"}, inplace=True)
        prompts_with_responses = merge_prompts_with_responses(prompts, llm_responses)
        prompts_with_responses_all = pd.concat(
            [prompts_with_responses_all, prompts_with_responses], ignore_index=True
        )

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/round2/prompt_with_response_{version}.xlsx"
    )
    prompts_with_responses_all.to_excel(prompts_response_file_path, index=False)

    # # Evaluate responses
    # evaluation_results = evaluate_responses(prompts_with_responses_all)

    # # Save evaluation results
    # evaluation_result_file_path = os.path.join(
    #     current_dir, f"../results/batch2/evaluation_results_{version}.txt"
    # )
    # with open(evaluation_result_file_path, "w") as file:
    #     file.write(str(evaluation_results))


if __name__ == "__main__":
    version = "v9"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/afrobarometer_sample.xlsx")

    input_data = {
        "data_file_path": data_file_path,
        "demographic_questions": [
            "Do you come from a rural or urban area?",
            "How old are you?",
            "What is your gender?",
            "What is your race?",
            "What is the primary language you speak in your home?",
            "What is your highest level of education?",
            "What is your religion, if any?",
            "What is your ethnic community or cultural group?",
            "Do you have a job that pays a cash income? If yes, is it full time or part time? If no, are you currently looking for a job?",
            "What is your main occupation? If unemployed, retired, or disabled, what was your last main occupation?",
            "Do you personally own a mobile phone? If not, does anyone else in your household own one?",
            "In general, how would you describe your own present living conditions?",
        ],
        "survey_questions": [
            "Over the past year, how often, if ever, have you or anyone in your family gone without Medicines or medical treatment?",
            "In the past 12 months, have you had contact with a public clinic or hospital?",
            "How easy or difficult was it to obtain the medical care or services you needed?",
            "Please tell me whether you personally or any other member of your household have became ill with, or tested positive for COVID-19 by the COVID-19 pandemic?",
            "Please tell me whether you personally or any other member of your household have temporarily or permanently lost a job, business, or primary source of income by the COVID-19 pandemic?",
            "Have you received a vaccination against COVID-19, either one or two doses?",
            "If a vaccine for COVID-19 is available , how likely are you to try to get vaccinated?",
            "What is the main reason that you would be unlikely to get a COVID-19 vaccine?",
            "How much do you trust the government to ensure that any vaccine for COVID-19 that is developed or offered to Nigerian citizens is safe before it is used in this country?",
        ],
        "survey_context": "You will simulate the persona of a human subject participating in a healthcare survey in Ghana. Please refer to the following information about your demographic profile, and respond to any questions in a consistent and coherent manner that matches with your demographic profile. Please also make sure you provide no explanations for your response and answer in the exact format that is asked of you.",
    }

    main(input_data)
