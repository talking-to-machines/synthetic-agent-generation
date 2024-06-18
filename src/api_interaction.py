import openai

def query_llm(prompt: dict, model: str = 'gpt-4') -> dict:
    """Call the OpenAI API with a prompt."""
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']
