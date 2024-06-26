from flask import Flask, request, jsonify
import os
from src.data_processing import (
    load_data,
    clean_data,
    merge_prompts_with_responses,
    create_batch_file,
)
from src.prompt_generation import generate_prompts
from src.api_interaction import query_llm
from src.evaluation import evaluate_responses
from openai import OpenAI
from config.settings import OPENAI_API_KEY


def main(request):
    # Load OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    # Load and preprocess data
    data = load_data(data_file_path)
    print(f"Loaded data: {data.shape}")
    data = clean_data(data, request["demographic_attributes"] + request["questions"])
    print(f"Data after cleaning: {data.shape}")

    # Generate prompts
    prompts = generate_prompts(
        client,
        data,
        request["survey_context"],
        request["demographic_attributes"],
        request["questions"],
    )
    print(f"Generated prompts: {prompts.shape}")
    # print(f"Example of prompt: {prompts.loc[0,:]}")

    # Create JSONL batch file
    batch_file_dir = create_batch_file(prompts)
    # print(f"batch_file_dir: {batch_file_dir}")

    # Get LLM responses
    responses = query_llm(client, batch_file_dir)
    print(f"Responses: {responses.shape}")
    # print(f"Example of response: {responses.loc[0,:]}")

    # Merge LLM responses with prompts
    prompts_with_responses = merge_prompts_with_responses(prompts, responses)
    print(f"Prompts with response: {prompts_with_responses.shape}")
    # print(f"Example of prompts with response: {prompts_with_responses.loc[0,:]}")

    # Evaluate responses
    evaluation_results = evaluate_responses(prompts_with_responses)

    return evaluation_results, prompts_with_responses


if __name__ == "__main__":
    version = "v1"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/ghana_wave_2_test.xlsx")
    evaluation_result_file_path = os.path.join(
        current_dir, f"../results/evaluation_results_{version}.txt"
    )
    prompts_response_file_path = os.path.join(
        current_dir, f"../results/prompt_with_response_{version}.xlsx"
    )
    input_data = {
        "data_file_path": data_file_path,
        "demographic_attributes": [
            "Do you come from a rural or urban area?",
            "What region do you come from?",
            "What is your gender?",
            "What is your race?",
            "What is the primary language you speak in your home?",
            "What is your highest level of education?",
            "What is your religion, if any?",
            "What is your ethnic community or cultural group?",
        ],
        "questions": [
            "If a vaccine for COVID-19 is available , how likely are you to try to get vaccinated?",
            "How much do you trust the government to ensure that any vaccine for COVID-19 that is developed or offered to Nigerian citizens is safe before it is used in this country?",
            "Please tell me whether you personally or any other member of your household have became ill with, or tested positive for COVID-19 by the COVID-19 pandemic?",
            "What is the main reason that you would be unlikely to get a COVID-19 vaccine?",
            "How old are you?",
        ],
        "survey_context": "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question.",
    }
    evaluation_results, prompts_with_responses = main(input_data)

    # Save evaluation results
    with open(evaluation_result_file_path, "w") as file:
        file.write(str(evaluation_results))

    # Save prompts with responses into Excel file
    prompts_with_responses.to_excel(prompts_response_file_path, index=False)
