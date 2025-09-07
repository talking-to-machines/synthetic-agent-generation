import os
import pandas as pd
from src.data_processing import load_data, create_batch_file, include_variable_names
from src.prompt_generation import generate_formatting_prompts
from src.api_interaction import batch_query
from openai import OpenAI
from config.settings import OPENAI_API_KEY


def main(request):
    # Load OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    data_file_path = os.path.join(request["raw_folder_path"], request["filename"])
    if data_file_path in os.listdir(request["formatted_folder_path"]):
        return None

    # Load and preprocess data
    data = load_data(data_file_path, drop_first_row=drop_first_row)

    # Append formatting instruction in system message
    prompts = generate_formatting_prompts(
        data,
        request["formatting_prompt"],
    )

    # Perform batch query for creating demographics-primed backstories for each subject
    batch_file_dir = create_batch_file(
        prompts,
        system_message_field="system_message",
        user_message_field="question_prompt",
        batch_file_name="batch_input_llm_formatting.jsonl",
    )

    llm_responses = batch_query(
        client,
        batch_input_file_dir=batch_file_dir,
        batch_output_file_dir="batch_output_llm_replication_experiment.jsonl",
    )

    # Define the lambda function to extract the results
    if request["study"] in ["duch_2023", "duch_2025"]:
        extract_responses = lambda x: pd.Series(
            {
                "Question 1": (
                    x.split("Question 1:")[1]
                    .split("\n")[0]
                    .strip()
                    .replace("[", "")
                    .replace("]", "")
                    if "Question 1:" in x
                    else ""
                ),
                "Question 2": (
                    x.split("Question 2:")[1].strip().replace("[", "").replace("]", "")
                    if "Question 2:" in x
                    else ""
                ),
            }
        )

        # Apply the lambda function to the 'responses' column
        llm_responses[["llm_response_question1", "llm_response_question2"]] = (
            llm_responses["query_response"].apply(extract_responses)
        )

        prompts_with_responses = pd.merge(
            left=prompts,
            right=llm_responses[
                ["custom_id", "llm_response_question1", "llm_response_question2"]
            ],
            on="custom_id",
        )
        data_with_responses = pd.merge(
            left=data,
            right=prompts_with_responses[
                ["ID", "llm_response_question1", "llm_response_question2"]
            ],
            on="ID",
            suffixes=("", "_y"),
        )

    elif request["study"] in [
        "milkman_control",
        "milkman_baseline",
        "campos",
        "duch_2023_synthetic",
    ]:
        extract_responses = lambda x: pd.Series(
            {
                "Question": (
                    x.split("Question:")[1]
                    .split("\n")[0]
                    .strip()
                    .replace("[", "")
                    .replace("]", "")
                    if "Question:" in x
                    else ""
                ),
            }
        )

        # Apply the lambda function to the 'responses' column
        llm_responses[["llm_response_question"]] = llm_responses[
            "query_response"
        ].apply(extract_responses)

        prompts_with_responses = pd.merge(
            left=prompts,
            right=llm_responses[["custom_id", "llm_response_question"]],
            on="custom_id",
        )
        data_with_responses = pd.merge(
            left=data,
            right=prompts_with_responses[["ID", "llm_response_question"]],
            on="ID",
            suffixes=("", "_y"),
        )

    else:
        raise ValueError(f"Study {request['study']} is not supported.")

    # Include variable names as new column headers
    if drop_first_row:
        data_with_response_headers = include_variable_names(
            data_with_responses, data_file_path
        )

    # Save prompts with responses into Excel file
    prompts_response_file_path = os.path.join(
        current_dir,
        f"../results/{request['experiment_round']}/formatted/{request['filename']}",
    )
    data_with_response_headers.to_excel(prompts_response_file_path, index=False)


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    study = "duch_2023_synthetic"  # duch_2023, duch_2025, milkman_control, milkman_baseline, campos, duch_2023_synthetic
    experiment_round = "round9"
    raw_folder_path = os.path.join(
        current_dir,
        f"../results/{experiment_round}",
    )
    formatted_folder_path = os.path.join(
        current_dir,
        f"../results/{experiment_round}/formatted",
    )
    prefix_string = ""
    drop_first_row = True

    input_data = {
        "raw_folder_path": raw_folder_path,
        "formatted_folder_path": formatted_folder_path,
        "experiment_round": experiment_round,
        "study": study,
    }

    if study == "milkman_control":
        ### Configuration for Milkman et al RCT - Control (START) ###
        input_data["filename"] = (
            "milkman_et_al_2024_metastudy_control_llama3.1_70b_s7.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following questions:
        Question: Did you receive a COVID-19 booster by early December 2022, within the first 30 days after the information on your profile was collected? Please, answer with one of the following options: Yes, No
        Response options: Yes, No
        The expected structured output format is:
        Question: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit the answers, or present the answer in a different order.
        - Your goal is to extract the definitive answers for the question and reformat them into the structured output as shown above.
        - If the answers are missing, output the missing answer as empty (e.g., Question:).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for Milkman et al RCT - Control (END) ###

    elif study == "milkman_baseline":
        ### Configuration for Milkman et al RCT - Baseline (START) ###
        input_data["filename"] = (
            "milkman_et_al_2024_metastudy_baseline_freeride_llama3.1_70b_s7.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following questions:
        Question: Did you receive a COVID-19 booster shot within 30 days after getting the first message from the CVS Pharmacy? Please, answer with one of the following options: Yes, No
        Response options: Yes, No
        The expected structured output format is:
        Question: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit the answers, or present the answer in a different order.
        - Your goal is to extract the definitive answers for the question and reformat them into the structured output as shown above.
        - If the answers are missing, output the missing answer as empty (e.g., Question:).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for Milkman et al RCT (END) ###

    elif study == "campos":
        ### Configuration for Campos Mercade RCT (START) ###
        input_data["filename"] = (
            "campos_mercade_et_al_2021_monetary_incentives_llama3.1_70b_s7.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following questions:
        Question: Have you got a first shot of a COVID-19 vaccine within the first 30 days after the vaccine became available to you? Available means that vaccinations started for people in your age group in your region. Please, answer with one of the following options: Yes, No
        Response options: Yes, No
        The expected structured output format is:
        Question: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit the answers, or present the answer in a different order.
        - Your goal is to extract the definitive answers for the question and reformat them into the structured output as shown above.
        - If the answers are missing, output the missing answer as empty (e.g., Question:).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for Campos Mercade RCT (END) ###

    elif study == "duch_2023":
        ### Configuration for COVID-19 RCT (START) ###
        input_data["filename"] = (
            "vaccine_financial_incentive_vaccinationstatus_llama3.1_8b_wo_intention_s6.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following two questions:
        Question 1: Have you received a COVID-19 vaccine?
        Response options: Yes, No
        Question 2: Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?
        Response options: Yes, No
        The expected structured output format is:
        Question 1: [Yes/No]
        Question 2: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit one or both answers, or present the answers in a different order.
        - Your goal is to extract the definitive answers for each question and reformat them into the structured output as shown above.
        - If one or both answers are missing, output the missing answer(s) as empty (e.g., Question 1: or Question 2: ).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for COVID-19 RCT (END) ###

    elif study == "duch_2023_synthetic":
        ### Configuration for COVID-19 RCT Synthetic - Heterogenity Analysis (START) ###
        input_data["filename"] = (
            "vaccine_financial_incentive_vaccinationstatus_llama3.1_8b_synthetic_s2.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following question:
        Question: Have you actually received a COVID-19 vaccine and can this be verified in the records of the Ghanaian District Health Offices?
        Response options: Yes, No
        The expected structured output format is:
        Question: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit the answers, or present the answer in a different order.
        - Your goal is to extract the definitive answers for the question and reformat them into the structured output as shown above.
        - If the answers are missing, output the missing answer as empty (e.g., Question:).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for COVID-19 RCT Synthetic - Heterogenity Analysis (END) ###

    elif study == "duch_2025":
        ### Configuration for TB Screening RCT (START) ###
        input_data["filename"] = (
            "duch_et_al_2025_ghana_tubercolosis_screening_deepseek_llama3.3_70b_s4.xlsx"
        )
        input_data[
            "formatting_prompt"
        ] = """Your task is to parse an unstructured text string generated by another LLM in response to the following two questions:
        Question 1: The Health District Tuberculosis screening team will be in your village within the next two weeks. Would you be willing to get the tuberculosis screening when the Health District Tuberculosis screening team is in your village?
        Response options: Yes, No, Do not know, Prefer not to say
        Question 2: Did you get the tuberculosis screening when the Health District Tuberculosis screening team was in your village?
        Response options: Yes, No
        The expected structured output format is:
        Question 1: [Yes/No/Do not know/Prefer not to say]
        Question 2: [Yes/No]
        Instructions:
        - The input text may include extraneous reasoning, commentary, or irrelevant content before or after the actual answers.
        - The unstructured text may sometimes omit one or both answers, or present the answers in a different order.
        - Your goal is to extract the definitive answers for each question and reformat them into the structured output as shown above.
        - If one or both answers are missing, output the missing answer(s) as empty (e.g., Question 1: or Question 2: ).
        - Do not include any additional text or commentary in your response; only output the structured answers.
        Parse the input accordingly and return your result in the exact format specified."""
        ### Configuration for TB Screening RCT (END) ###

    else:
        raise ValueError(f"Study {study} is not supported.")

    main(input_data)
