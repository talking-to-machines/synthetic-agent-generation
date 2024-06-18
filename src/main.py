from src.data_processing import load_data, clean_data, preprocess_data
from src.prompt_generation import generate_prompts
from src.api_interaction import query_llm
from src.evaluation import evaluate_responses

def main():
    # Load and preprocess data
    data = load_data('data/survey.csv')
    data = clean_data(data)
    data = preprocess_data(data)

    # Generate prompts
    prompts = generate_prompts(data, ['col1', 'col2'], ['target_col'])

    # Get LLM responses
    predictions = []
    ground_truths = []
    for prompt, target in prompts:
        response = query_llm(prompt)
        predictions.append(response)
        ground_truths.append(target['target_col'])

    # Evaluate responses
    results = evaluate_responses(predictions, ground_truths)
    print(f"Evaluation Results: {results}")

if __name__ == "__main__":
    main()
