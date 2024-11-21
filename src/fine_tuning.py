import os
from src.data_processing import load_data, clean_data, create_finetune_batch_file
from src.prompt_generation import generate_prompts
from openai import OpenAI
from config.settings import OPENAI_API_KEY


def main(request):
    # Load OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    # Load and preprocess data
    data = load_data(data_file_path)
    data = clean_data(
        data, request["demographic_questions"] + request["survey_questions"]
    )

    # Generate demographic prompts
    prompts = generate_prompts(
        client,
        data,
        request["survey_context"],
        request["demographic_questions"],
        request["survey_questions"],
    )

    # Create batch file for fine-tuning
    create_finetune_batch_file(
        prompts,
        system_message_field="system_message",
        user_message_field="question_prompt",
        user_response_field="user_response",
        batch_file_name="batch_finetune_llm_survey_response.jsonl",
    )


if __name__ == "__main__":
    version = "v4_finetune"
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, "../data/afrobarometer_train.xlsx")

    input_data = {
        "data_file_path": data_file_path,
        "demographic_questions": [
            "Do you come from a rural or urban area?",
            "How old are you?",
            "What is your gender?",
            "What is your highest level of education?",
            "What is your religion, if any?",
            "What region do you come from?",
            "Do you feel close to any particular political party?",
            "When you get together with your friends or family, how often would you say you discuss political matters?",
            "Latitude",
            "Longitude",
            "What is the distance to the nearest health clinic from your location in kilometers?",
            "What district do you live in?",
            "What percentage of the population in your district voted for the National Democratic Congress (NDC)?",
            "What percentage of the population in your district voted for the New Patriotic Party (NPP)?",
        ],
        "survey_questions": [
            "In the past 12 months, have you had contact with a public clinic or hospital?",
            "Have you received a vaccination against COVID-19, either one or two doses?",
        ],
        "survey_context": "Please put yourself in the shoes of a human subject participating in a healthcare survey in Ghana. You will be provided with a demographic profile that describes the area/region/district where you live, your gender, the highest education level you achieved, your religion, the distance to your nearest health clinic, the political party you feel closest to, and the percentage vote for the New Patriotic Party in your district. The information will be provided to you in the format of a survey interview. You will see a question from the “Interviewer:” and then your human subject response will be preceded by “Me:”. We also provide you with the demographic profile of three other subjects and their responses to several COVID-19 vaccination-related questions in the same survey interview format. Lastly, we will provide you with some general findings from past studies on Ghana’s COVID-19 vaccination efforts. After you receive your complete human subject profile, you will be asked whether you received the COVID-19 vaccination. Please provide a consistent and coherent response using all the information provided. It is crucial for you to accurately replicate the response of a human subject that has the demographic profile you are provided. The human subject response will vary depending on their demographic profile. If you are unsure of an answer, provide a plausible response that is based on all of the information available to you. Respond to each question in the exact format specified and do not add any information beyond what is requested.",
    }

    main(input_data)
