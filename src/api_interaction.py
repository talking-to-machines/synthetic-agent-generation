import openai
import pandas as pd


def query_llm(prompts: pd.DataFrame) -> pd.DataFrame:
    """
    Query the LLM with prompts and return the responses.

    Parameters:
    prompts (pd.DataFrame): The prompts to query the LLM with.

    Returns:
    pd.DataFrame: The prompts with the corresponding LLM responses.
    """
    responses = []
    for prompt in prompts["prompt"]:
        response = query(prompt)
        responses.append(response)

    prompts["response"] = responses

    return prompts


def query(prompt: str, model: str = "gpt-4") -> str:
    """
    Call the OpenAI API with a prompt.

    Parameters:
    prompt (str): The prompt to query the LLM with.
    model (str): The model version.

    Returns:
    str: The response from the LLM.
    """
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=150)
    return response["choices"][0]["text"]
