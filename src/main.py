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
    data = clean_data(data, request["demographic_attributes"] + request["questions"])

    # Generate prompts
    prompts = generate_prompts(
        client,
        data,
        request["survey_context"],
        request["demographic_attributes"],
        request["questions"],
    )

    # Create JSONL batch file
    batch_file_dir = create_batch_file(prompts)

    # Get LLM responses
    responses = query_llm(client, batch_file_dir)

    # Merge LLM responses with prompts
    prompts_with_responses = merge_prompts_with_responses(prompts, responses)

    # Evaluate responses
    evaluation_results = evaluate_responses(prompts_with_responses)

    return jsonify(evaluation_results)


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/ghana_wave_2_sample.xlsx")
    input_data = {
        "data_file_path": data_file_path,
        "demographic_attributes": [],
        "questions": [],
        "survey_context": "INSERT CONTEXT HERE",
        "openai_key": "",
    }
    evaluation_results = main(input_data)
    print(evaluation_results)
