def generate_prompts(df: pd.DataFrame, prompt_columns: list, target_columns: list) -> list:
    """Generate prompts from the survey data."""
    prompts = []
    for index, row in df.iterrows():
        prompt = {col: row[col] for col in prompt_columns}
        target = {col: row[col] for col in target_columns}
        prompts.append((prompt, target))
    return prompts
