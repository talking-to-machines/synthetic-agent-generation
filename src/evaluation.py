from sklearn.metrics import accuracy_score

def evaluate_responses(predictions: list, ground_truths: list) -> dict:
    """Evaluate the LLM's responses."""
    accuracy = accuracy_score(ground_truths, predictions)
    # Add more evaluation metrics as needed
    return {'accuracy': accuracy}
