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
    data = clean_data(data, request["survey_questions"])

    prompts_with_responses_all = pd.DataFrame()
    batch_size = 10
    for i in tqdm(range(0, len(data), batch_size)):
        batch_data = data[i : i + batch_size].reset_index(drop=True)

        # Generate demographic prompts
        prompts = generate_prompts(
            client,
            batch_data,
            request["survey_context"],
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

    # Evaluate responses
    evaluation_results = evaluate_responses(prompts_with_responses_all)

    return evaluation_results, prompts_with_responses_all


if __name__ == "__main__":
    version = "v3"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/ghana_wave_2_sample.xlsx")

    input_data = {
        "data_file_path": data_file_path,
        "survey_questions": [
            "How old are you?",
            "What is your gender?",
            "What is your race?",
            "What is your highest level of education?",
            "Do you personally own a mobile phone? If not, does anyone else in your household own one?",
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
        "survey_context": "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question.",
    }

    evaluation_results, prompts_with_responses = main(input_data)

    # Save evaluation results
    evaluation_result_file_path = os.path.join(
        current_dir, f"../results/evaluation_results_{version}.txt"
    )
    with open(evaluation_result_file_path, "w") as file:
        file.write(str(evaluation_results))

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/prompt_with_response_{version}.xlsx"
    )
    prompts_with_responses.to_excel(prompts_response_file_path, index=False)
