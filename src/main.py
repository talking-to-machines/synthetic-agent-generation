from flask import Flask, request, jsonify
import os
from src.data_processing import load_data, clean_data
from src.prompt_generation import generate_prompts
from src.api_interaction import query_llm
from src.evaluation import evaluate_responses


def main(request):
    # Load and preprocess data
    data = load_data(data_file_path)
    data = clean_data(data, request["demographic_attributes"] + request["questions"])

    # Generate prompts
    prompts = generate_prompts(
        data,
        request["survey_context"],
        request["demographic_attributes"],
        request["questions"],
    )

    # Get LLM responses
    prompts_with_response = query_llm(prompts)

    # Evaluate responses
    results = evaluate_responses(prompts_with_response)

    return jsonify({"Evaluation Results": results})


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
    main(input_data)
