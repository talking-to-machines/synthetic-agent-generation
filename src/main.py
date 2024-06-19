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
    prompts = generate_prompts(data, ["col1", "col2"], ["target_col"])

    # Get LLM responses
    predictions = []
    ground_truths = []
    for prompt, target in prompts:
        response = query_llm(prompt)
        predictions.append(response)
        ground_truths.append(target["target_col"])

    # Evaluate responses
    results = evaluate_responses(predictions, ground_truths)
    return jsonify({"Evaluation Results": results})


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/ghana_wave_2_sample.xlsx")
    input_data = {
        "data_file_path": data_file_path,
        "demographic_attributes": [],
        "questions": [],
        "openai_key": "",
    }
    main(input_data)
