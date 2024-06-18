# Import necessary libraries
import pandas as pd

# Read the CSV file
data = pd.read_csv("../Data/ghana_round_9/kitchen_sink_first_person_ghana9_add_var.csv")

# Define the list of real answers
real_answers = [
    "Always", "Just once or twice", "Many times", "Never", "Several times", 
    "No", "Yes", 
    "Difficult", "Easy", "Very Difficult", "Very easy",
    "A few times", "Never", "Often", "Once or twice",
    "A little bit", "A lot", "No contact", "Not at all", "Somewhat",
    "Health-related issues such as health sickness/disease COVID-19 and AIDS", "Issues other than health such as the economy, food/agriculture, infrastructure, public services, county's governance and climate", "Nothing/ no problems",
    "Somewhat likely", "Somewhat unlikely", "Very likely", "Very unlikely",
    "Afraid of vaccines in general", "Allergic to vaccines", "COVID doesn't exist / COVID is not real",  "Don't like needles",  "Don't trust the vaccine source / Will wait for other vaccines", "Don't trust the vaccine/worried about getting fake or counterfeit vaccine", "Effective treatments for COVID are or will be available", "God will protect me", "I already had COVID and believe I am immune", "I am at no risk or low risk for getting COVID / Small chance of contracting COVID", "I will get the vaccine later", "I will wait until others have been vaccinated", "It is too difficult to get the vaccine, e.g. have to travel far", "Not worried about COVID / COVID is not serious or life-threatening/not deadly", "People are being experimented on with vaccines", "Religious objections to vaccines in general or to the COVID vaccine", "Some other reason", "Vaccine is not effective / Vaccinated people can still get COVID", "Vaccine is not safe", "Vaccine may cause COVID", "Vaccine may cause infertility", "Vaccine may cause other bad side effects", "Vaccine was developed too quickly", "Vaccine will be too expensive", "Vaccines are being used to control or track people",
    "A lot", "Just a little", "Not at all", "Somewhat",
    "Completely free", "Not at all free", "Not very free", "Somewhat free",
    "A few times", "Never", "Often", "Only once",
    "Do not know", "Fairly satisfied", "Not at all satisfied", "Not very satisfied", "The country is not a democracy", "Very satisfied",
    "Always", "Never", "Often", "Rarely",
    "Always", "Never", "Often", "Sometimes",
    "Community leaders", "Other", "Other family members", "Religious leaders", "The local administration", "The Neighbourhood including neighbourhood watch", "The police",
    "A few times a month", "A few times a week", "Every day", "Less than once a month", "Never"
]

# Number of removed observations
num_removed_observations = len(data) - data['Response'].isin(real_answers).sum()

# Print number of removed observations
print(f"Number of removed observations: {num_removed_observations}")

# Filter the data
filtered_data = data[data['Response'].isin(real_answers)]


# Approahc 3: 
# Me and interviewer
# We use the following questions 

# selected questions: 
# covariates: "Q1" , "Q100" ,  "Q101" , "Q94"
# other high priority questions: 
# # 8. When you get together with your friends or family, how often would you say you discuss political matters?
# 4A. In general, how would you describe: The present economic condition of this country?
# 9A. In this country, how free are you: to say what you think?
 
#Q6C : Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment?
#Q41A : In the past 12 months, have you had contact with a public clinic or hospital?
#Q41B : How easy or difficult was it to obtain the medical care or services you needed? 
#Q41C : How often, if ever, did you have to pay a bribe, give a gift, or do a favor for a health worker or clinic or hospital staff in order to get the medical care or services you needed?
#Q41D : In general, when dealing with health workers and clinic or hospital staff, how much do you feel you can trust them?
#Q41G  


# Unique questions
unique_questions = data['Question'].unique()

# Filter data where Question is in the specified list
data_res = data[data['Question'].isin(["Q6C", "Q41A", "Q41D"])]

# Get unique IDs
id_vec = data_res['ID_'].unique()

# Initialize a list to collect valid IDs
full_set_id = []

# Iterate over each unique ID
for check_now in id_vec:
    # Filter data for the current ID
    val_set = data_res[data_res['ID_'] == check_now]
    # If the number of rows for this ID is 3, add it to the full_set_id
    if len(val_set) == 3:
        full_set_id.append(check_now)

# Number of NA values (IDs not having exactly 3 records)
num_na = len(id_vec) - len(full_set_id)

# Filter data_res for rows where ID_ is in full_set_id
data_res = data_res[data_res['ID_'].isin(full_set_id)]

# create prompts
#list of questions: 
# covariates questions: 
# "Q1"  How old are you?
# "Q100" What is your gender?
# "Q101" What is your race?
# "Q94" What is your highest level of education?

# 8. When you get together with your friends or family, how often would you say you discuss political matters?
# 4A. In general, how would you describe: The present economic condition of this country?
# 9A. In this country, how free are you: to say what you think?

#Q6C : Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment?
#Q41A : In the past 12 months, have you had contact with a public clinic or hospital?
#Q41B : How easy or difficult was it to obtain the medical care or services you needed? 
#Q41C : How often, if ever, did you have to pay a bribe, give a gift, or do a favor for a health worker or clinic or hospital staff in order to get the medical care or services you needed?
#Q41D : In general, when dealing with health workers and clinic or hospital staff, how much do you feel you can trust them?

q1_question = 'Interviewer: What is your age in years?'
q100_question = 'Interviewer: What is your gender? Please respond with Man or Woman '
q101_question = 'Interviewer: What is your race? Please respond with  Black or Coloured  '
q94_question = 'Interviewer: What is your highest level of education? Please respond with university, diploma, secondary, primary school or no formal schooling   '
q8_question = 'Interviewer: When you get together with your friends or family, how often would you say you discuss political matters? Please respond with  Occasionally, Never or Frequently   '
q4a_question = 'Interviewer: In general, how would you describe: The present economic condition of this country? Please respond with Very good, Fairly good, Neither good nor bad, Fairly bad or Very bad  '
q9a_question = 'Interviewer: In this country, how free are you: to say what you think?  Please respond with  Completely free, Somewhat free, Not very free or Not at all free  '
q6c_question = 'Interviewer: Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment?  Please respond with  Always, Many times , Several times, Just once or twice or Never   '  
q41a_question = 'Interviewer: In the past 12 months, have you had contact with a public clinic or hospital? Please respond with  Yes or No '  
q41d_question = 'Interviewer: In general, when dealing with health workers and clinic or hospital staff, how much do you feel you can trust them? Please respond with   A lot, A little bit, Somewhat, No contact or Not at all   '  



# Assume data_res and data are pandas DataFrames

# Education recoded:
data_res['education'] = data_res['Q94'].apply(lambda x: 'no formal schooling' if x in ["No formal schooling", "Informal schooling only (including Koranic schooling)"] else
                                                    'primary school' if x in ["Some primary schooling", "Primary school completed"] else
                                                    'secondary' if x in ["Intermediate school or Some secondary school / high school", "Secondary school / high school completed"] else
                                                    'diploma' if x in ["Post-secondary qualifications, other than university e.g. a diploma or degree from a polytechnic or college"] else
                                                    'university')

# Race recoded:
data_res['race'] = data_res['Q101'].apply(lambda x: 'Black' if x == "Black / African" else 'Coloured')

# Unique values
unique_education = data_res['education'].unique()
print("Unique education values:", unique_education)

# Unique responses
unique_responses_Q6C = data[data['Question'] == "Q6C"]['Response'].unique()
#"Always", "Many times" , "Several times", "Just once or twice", "Never"  
unique_responses_Q41A = data[data['Question'] == "Q41A"]['Response'].unique()
# "Yes", "No", "Refused to Answer"
unique_responses_Q41B = data[data['Question'] == "Q41B"]['Response'].unique()
# "Very easy", "Easy", "Difficult", "Very Difficult" 
unique_responses_Q41C = data[data['Question'] == "Q41C"]['Response'].unique()
# "Often", "A few times", "Once or twice", "Never" 
unique_responses_Q41D = data[data['Question'] == "Q41D"]['Response'].unique()
#  "A lot", "A little bit", "Somewhat", "No contact", "Not at all"  


# Table for Q94
q94_counts = data['Q94'].value_counts()

# Initialize the list for the new prompt file
new_prompt_file = []

# Get unique IDs
id_vec = data_res['ID_'].unique()

# Iterate over each unique ID
for i in range(len(id_vec)):
    check_now = id_vec[i]
    val_set = data_res[data_res['ID_'] == check_now]

    # Extract answers
    q1_answer = val_set['Q1'].unique()
    q100_answer = val_set['Q100'].unique()
    q101_answer = val_set['race'].unique()
    q94_answer = val_set['education'].unique()
    q8_answer = val_set['Q8'].unique()
    q4a_answer = val_set['Q4A'].unique()
    q9a_answer = val_set['Q9A'].unique()
    q6c_answer = val_set[val_set['Question'] == 'Q6C']['Response']
    q41a_answer = val_set[val_set['Question'] == 'Q41A']['Response']
    q41d_answer = val_set[val_set['Question'] == 'Q41D']['Response']

    # Assemble text prompts
    text1 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question}'])
    text2 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q41a_question}'])
    text3 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q6c_question}'])
    text4 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q9a_question}'])
    text5 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q4a_question}'])
    text6 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q8_question}'])
    text7 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q94_question}'])
    text8 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q100_question} Me: {q100_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q101_question}'])
    text9 = ' '.join([f'{q1_question} Me: {q1_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{q6c_question} Me: {q6c_answer}', f'{q41a_question} Me: {q41a_answer}', f'{q41d_question} Me: {q41d_answer}', f'{q100_question}'])
    text10 = ' '.join([f'{q100_question} Me: {q100_answer}', f'{q101_question} Me: {q101_answer}', f'{q94_question} Me: {q94_answer}', f'{q8_question} Me: {q8_answer}', f'{q4a_question} Me: {q4a_answer}', f'{q9a_question} Me: {q9a_answer}', f'{



# Function to create chat completion with OpenAI API
def create_chat_completion(messages):
    return OpenAI.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",  # Model name
        messages=messages,
        temperature=1.0  # Temperature parameter
    )

# Assuming you have loaded your data into 'prompt_set' DataFrame

# Convert prompt_set to DataFrame if not already
prompt_set = pd.DataFrame(prompt_set)

# Initialize list to store results
initial_forecasts_list_with_sys_msg = []

# Iterate over each row in prompt_set
for i in range(prompt_set.shape[0]):
    sel_subject = prompt_set.iloc[i, :]

    # Initialize list to store chat outcomes for each question
    subject_list = []

    # Iterate over columns 2 to 11 (assuming zero-indexed columns)
    for j in range(1, 11):
        # Construct messages for OpenAI API
        messages = [
            {"role": "system", "content": "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question."},
            {"role": "user", "content": sel_subject[j]}
        ]

        # Request chat completion from OpenAI API
        chat_outcome = create_chat_completion(messages)

        # Append generated response to subject_list
        subject_list.append(chat_outcome['choices'][0]['message']['content'])

    # Convert subject_list to DataFrame
    subject_results = pd.DataFrame(subject_list)

    # Rename columns of subject_results
    subject_results.columns = ["Q41d_GPT35", "Q41a_GPT35", "Q6C_GPT35", "Q9A_GPT35", "Q4A_GPT35", "Q8_GPT35", "Q94_GPT35", "Q101_GPT35", "Q100_real", "Q1_GPT35"]

    # Append subject_results to initial_forecasts_list_with_sys_msg
    initial_forecasts_list_with_sys_msg.append(subject_results)

    # Print progress
    print(f"Processed row {i + 1}")

# Concatenate results into a single DataFrame
results = pd.concat(initial_forecasts_list_with_sys_msg, ignore_index=True)

# Assuming results35 is the final DataFrame to save or use
results35 = results

# Saving results as CSV
results35.to_csv("240520_ResultsGPT35_FullSample.csv", index=False)


import pandas as pd
import os
from openai import OpenAI

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = ''

# Function to create chat completion with OpenAI API
def create_chat_completion(messages):
    return OpenAI.ChatCompletion.create(
        model="gpt-4",  # Model name: gpt-4, gpt-4o, etc.
        messages=messages,
        temperature=1.0  # Temperature parameter
    )

# Assuming 'prompt_set' is your DataFrame loaded with data

# Convert 'prompt_set' to DataFrame if not already
prompt_set = pd.DataFrame(prompt_set)

# Initialize list to store results
initial_forecasts_list_with_sys_msg_40_turbo = []

# Iterate over each row in 'prompt_set'
for i in range(prompt_set.shape[0]):
    sel_subject = prompt_set.iloc[i, :]

    # Initialize list to store chat outcomes for each question
    subject_list = []

    # Iterate over columns 2 to 11 (assuming zero-indexed columns)
    for j in range(1, 11):
        # Construct messages for OpenAI API
        messages = [
            {"role": "system", "content": "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question."},
            {"role": "user", "content": sel_subject[j]}
        ]

        # Request chat completion from OpenAI API
        chat_outcome = create_chat_completion(messages)

        # Append generated response to subject_list
        subject_list.append(chat_outcome['choices'][0]['message']['content'])

    # Convert subject_list to DataFrame
    subject_results = pd.DataFrame(subject_list)

    # Rename columns of subject_results
    subject_results.columns = ["Q41d_GPT35", "Q41a_GPT35", "Q6C_GPT35", "Q9A_GPT35", "Q4A_GPT35", "Q8_GPT35", "Q94_GPT35", "Q101_GPT35", "Q100_real", "Q1_GPT35"]

    # Append subject_results to initial_forecasts_list_with_sys_msg_40_turbo
    initial_forecasts_list_with_sys_msg_40_turbo.append(subject_results)

    # Print progress
    print(f"Processed row {i + 1}")

# Concatenate results into a single DataFrame
results = pd.concat(initial_forecasts_list_with_sys_msg_40_turbo, ignore_index=True)

# Saving results as CSV
results.to_csv("240520_Results_GPT40_turbo_FullSample.csv", index=False)

# If you want to save as RData, you would need to use a different library or format
# (Python doesn't have a native RData format, so you would need to handle this separately)


# Read data into a DataFrame
combo_file = pd.read_csv("your_file.csv")

# Convert columns to long format
long_data = pd.melt(combo_file, value_vars=["Q100_GPT35_adj", "Q100_real"], var_name="variable", value_name="value")

# Create a bar plot
plt.figure(figsize=(8, 6))
sns.barplot(data=long_data, x="value", y=None, hue="variable", dodge=True)
plt.title("Comparison of Categories")
plt.xlabel("Categories")
plt.ylabel("Count")
plt.legend(labels=["GPT35 Adj", "Real"])
plt.show()

# Create a faceted bar plot
plt.figure(figsize=(8, 6))
sns.barplot(data=long_data, x="value", y=None, hue="value", dodge=False)
plt.title("Bar Chart of Each Variable")
plt.xlabel("Categories")
plt.ylabel("Count")
plt.legend().remove()
plt.show()

# Create histograms
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.hist(combo_file["Q100_GPT35_adj"], bins=20)
plt.title("Histogram of Q100_GPT35_adj")
plt.subplot(1, 2, 2)
plt.hist(combo_file["Q100_real"], bins=20)
plt.title("Histogram of Q100_real")
plt.tight_layout()
plt.show()

# Calculate percentages
data_percent = combo_file["Q100_GPT35_adj"].value_counts(normalize=True).reset_index()
data_percent.columns = ["Category", "Percentage"]
data_percent["Percentage"] *= 100

# Plot percentages
plt.figure(figsize=(8, 6))
sns.barplot(data=data_percent, x="Category", y="Percentage", dodge=False)
plt.title("Percentage of Each Category in Q100_GPT35_adj")
plt.xlabel("Category")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=45, ha="right")
plt.show()

# Print column names
print(combo_file.columns)

# Convert columns to lowercase
combo_file.loc[:, "Q1_GPT35":"Q20_real"] = combo_file.loc[:, "Q1_GPT35":"Q20_real"].apply(lambda x: x.astype(str).str.lower())

# Access a specific column
print(combo_file["Q1_GPT35"])


import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

# Set seed for reproducibility
np.random.seed(123)

# Read data into a DataFrame
combo_file = pd.read_csv("your_file.csv")

# Select 1000 random rows for in-sample and out-sample
random_indices = np.random.choice(combo_file.index, size=1000, replace=False)
in_sample = combo_file.loc[random_indices, :]
out_sample = combo_file.drop(random_indices)

# Print random indices
print(random_indices)

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2_corrected = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    cramers_v = np.sqrt(phi2_corrected / min((k - 1), (r - 1)))
    return cramers_v

# Extract real and GPT35 variable names
real_vars = [col for col in combo_file.columns if col.endswith("_real")]
gpt35_vars = [col.replace("_real", "_GPT40_adj") for col in real_vars]

# Function to extract the base question name
def extract_base_name(var_name):
    return var_name.split("_")[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(combo_file[real_var_i], combo_file[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": real_var_i,
                "Comparison": real_var_j,
                "Model": "Real",
                "CramersV": cramer_real
            })

# Calculate Cramér's V for each GPT35 variable against all real variables
for gpt35_var in gpt35_vars:
    base_name_i = extract_base_name(gpt35_var)
    for real_var_j in real_vars:
        if base_name_i != extract_base_name(real_var_j):
            cramer_gpt35 = calculate_cramers_v(combo_file[gpt35_var], combo_file[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": gpt35_var,
                "Comparison": real_var_j,
                "Model": "GPT35",
                "CramersV": cramer_gpt35
            })

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Melt the DataFrame for plotting
results_melted = pd.melt(results_df, id_vars=["BaseName", "Variable", "Comparison", "Model"], value_name="CramersV")

# Filter out rows where Cramér's V is NaN
results_melted = results_melted.dropna(subset=["CramersV"])

# Plot the results
plt.figure(figsize=(12, 8))
sns.pointplot(data=results_melted, x="CramersV", y="Comparison", hue="Model", join=False, dodge=0.3, markers=["o", "s"], palette="muted")
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.subplots_adjust(left=0.1, right=0.85, bottom=0.2, top=0.9)
plt.show()

# Print Cramér's V for a specific variable
print(round(results_melted.loc[(results_melted["Variable"] == "Q1_real"), "CramersV"].values, 2))

# Print the provided information
print("Please keep in mind that the Cramers V-correlations of age in the real data with other questions are the following:  with gender is 0.20, with race 0.18, with education 0.24, with the question When you get together with your friends or family, how often would you say you discuss political matters? 0.16, with the present economic condition of this country 0.16, with the question In this country, how free are you: to say what you think? 0.16, with the question Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment? 0.16, with the question In the past 12 months, have you had contact with a public clinic or hospital? 0.20, and with the question In general, when dealing with health workers and clinic or hospital staff, how much do you feel you can trust them? 0.19.")


import os
import openai
from tqdm import tqdm

# Set your OpenAI API key
openai.api_key = ""

# Read data into a DataFrame (assuming you have already done this)
# out_sample = ...

# Print the first prompt in out_sample
print(out_sample["Q1_prompt"].iloc[0])

# Add "please respond numeric" to the end of each prompt
out_sample["Q1_prompt"] = out_sample["Q1_prompt"].apply(lambda x: x + " please respond numeric")

# Function to create a chat completion
def create_chat_completion(model, messages, temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

# Initialize a list to store the initial forecasts
initial_forecasts_list_with_sys_msg_35 = []

# Loop through the rows of out_sample
for i in tqdm(range(1170, out_sample.shape[0])):  # dim(prompt_set)[1]
    sel_subject = out_sample.iloc[i, :]
    subject_list = []
    for j in range(2, 12):
        system_message = "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question. Please keep in mind that the Cramers V-correlations of age in the real data with other questions are the following:  with gender is 0.20, with race 0.18, with education 0.24, with the question When you get together with your friends or family, how often would you say you discuss political matters? 0.16, with the present economic condition of this country 0.16, with the question In this country, how free are you: to say what you think? 0.16, with the question Over the past year, how often, if ever, have you or anyone in your family gone without: Medicines or medical treatment? 0.16, with the question In the past 12 months, have you had contact with a public clinic or hospital? 0.20, and with the question In general, when dealing with health workers and clinic or hospital staff, how much do you feel you can trust them? 0.19."
        user_message = sel_subject.iloc[j]

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        chat_outcome = create_chat_completion(
            model="gpt-3.5-turbo-0613",  # "gpt-3.5-turbo-0613", "gpt-4", "gpt-3.5-turbo-1106""gpt-4o"
            messages=messages,
            temperature=1,
        )
        subject_list.append(chat_outcome)

    subject_results = pd.DataFrame([subject_list], columns=[
        "Q41d_GPT35", "Q41a_GPT35", "Q6C_GPT35", "Q9A_GPT35", "Q4A_GPT35", "Q8_GPT35",
        "Q94_GPT35", "Q101_GPT35", "Q100_real", "Q1_GPT35"
    ])
    initial_forecasts_list_with_sys_msg_35.append(subject_results)

    # Print the current row number
    print(i)



# Rename columns
results35c.rename(columns={"Q100_GPT35": "Q100_GPT35_adj"}, inplace=True)

# Preprocess GPT-3.5 results
results35c["Q41d_GPT35"] = results35c["Q41d_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q41a_GPT35"] = results35c["Q41a_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q6C_GPT35"] = results35c["Q6C_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q9A_GPT35"] = results35c["Q9A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q4A_GPT35"] = results35c["Q4A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q8_GPT35"] = results35c["Q8_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q94_GPT35"] = results35c["Q94_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q101_GPT35"] = results35c["Q101_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q100_GPT35_adj"] = results35c["Q100_GPT35_adj"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results35c["Q1_GPT35"] = results35c["Q1_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)

# Preprocess GPT-4 results
results40c = results40c.astype(object)
results40c.rename(columns={"Q100_GPT35": "Q100_GPT40"}, inplace=True)
results40c["Q41d_GPT40"] = results40c["Q41d_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q41a_GPT40"] = results40c["Q41a_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q6C_GPT40"] = results40c["Q6C_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q9A_GPT40"] = results40c["Q9A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q4A_GPT40"] = results40c["Q4A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q8_GPT40"] = results40c["Q8_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q94_GPT40"] = results40c["Q94_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q101_GPT40"] = results40c["Q101_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q100_GPT40"] = results40c["Q100_GPT40"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results40c["Q1_GPT40"] = results40c["Q1_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)

# Preprocess GPT-4 turbo results
results_40_turbo = results_40_turbo.astype(object)
results_40_turbo.rename(columns={"Q100_GPT35": "Q100_GPT40t"}, inplace=True)
results_40_turbo["Q41d_GPT40t"] = results_40_turbo["Q41d_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q41a_GPT40t"] = results_40_turbo["Q41a_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q6C_GPT40t"] = results_40_turbo["Q6C_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q9A_GPT40t"] = results_40_turbo["Q9A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q4A_GPT40t"] = results_40_turbo["Q4A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q8_GPT40t"] = results_40_turbo["Q8_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q94_GPT40t"] = results_40_turbo["Q94_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q101_GPT40t"] = results_40_turbo["Q101_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q100_GPT40t"] = results_40_turbo["Q100_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q1_GPT40t"] = results_40_turbo["Q1_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)


# Combine datasets
combo_file_c = pd.concat([out_sample, results35c, results40c], axis=1)

# Adjust GPT-3.5 predictions
combo_file_c["Q41d_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q41d_GPT35"] if row["Q41d_GPT35"].lower() in row["Q41d_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q41a_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q41a_GPT35"] if row["Q41a_GPT35"].lower() in row["Q41a_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q6C_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q6C_GPT35"] if row["Q6C_GPT35"].lower() in row["Q6C_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q9A_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q9A_GPT35"] if row["Q9A_GPT35"].lower() in row["Q9A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q4A_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q4A_GPT35"] if row["Q4A_GPT35"].lower() in row["Q4A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q8_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q8_GPT35"] if row["Q8_GPT35"].lower() in row["Q8_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q94_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q94_GPT35"] if row["Q94_GPT35"].lower() in row["Q94_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q101_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q101_GPT35"] if row["Q101_GPT35"].lower() in row["Q101_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q100_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q100_GPT35"] if row["Q100_GPT35"].lower() in row["Q100_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q1_GPT35_adj"] = combo_file_c.apply(lambda row: row["Q1_GPT35"] if row["Q1_GPT35"].lower() in row["Q1_real"].str.lower().unique() else pd.NA, axis=1)

# Adjust GPT-4 predictions
combo_file_c["Q41d_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q41d_GPT40"] if row["Q41d_GPT40"].lower() in row["Q41d_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q41a_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q41a_GPT40"] if row["Q41a_GPT40"].lower() in row["Q41a_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q6C_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q6C_GPT40"] if row["Q6C_GPT40"].lower() in row["Q6C_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q9A_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q9A_GPT40"] if row["Q9A_GPT40"].lower() in row["Q9A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q4A_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q4A_GPT40"] if row["Q4A_GPT40"].lower() in row["Q4A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q8_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q8_GPT40"] if row["Q8_GPT40"].lower() in row["Q8_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q94_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q94_GPT40"] if row["Q94_GPT40"].lower() in row["Q94_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q101_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q101_GPT40"] if row["Q101_GPT40"].lower() in row["Q101_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q100_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q100_GPT40"] if row["Q100_GPT40"].lower() in row["Q100_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q1_GPT40_adj"] = combo_file_c.apply(lambda row: row["Q1_GPT40"] if row["Q1_GPT40"].lower() in row["Q1_real"].str.lower().unique() else pd.NA, axis=1)


import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2_corrected = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    cramers_v = np.sqrt(phi2_corrected / min((k - 1), (r - 1)))
    return cramers_v

# Extract real and GPT35 variable names
real_vars = [col for col in combo_file_c.columns if col.endswith("_real")]
gpt35_vars = [col.replace("_real", "_GPT35_adj") for col in real_vars]

# Function to extract the base question name
def extract_base_name(var_name):
    return var_name.split("_")[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(combo_file_c[real_var_i], combo_file_c[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": real_var_i,
                "Comparison": real_var_j,
                "Model": "Real",
                "CramersV": cramer_real
            })

# Calculate Cramér's V for each GPT35 variable against all real variables
for gpt35_var in gpt35_vars:
    base_name_i = extract_base_name(gpt35_var)
    for real_var_j in real_vars:
        if base_name_i != extract_base_name(real_var_j):
            cramer_gpt35 = calculate_cramers_v(combo_file_c[gpt35_var], combo_file_c[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": gpt35_var,
                "Comparison": real_var_j,
                "Model": "GPT35",
                "CramersV": cramer_gpt35
            })

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Melt the DataFrame for plotting
results_melted = pd.melt(results_df, id_vars=["BaseName", "Variable", "Comparison", "Model"], value_name="CramersV")

# Filter out rows where Cramér's V is NaN
results_melted = results_melted.dropna(subset=["CramersV"])

# Plot the results
plt.figure(figsize=(12, 8))
sns.pointplot(data=results_melted, x="CramersV", y="Comparison", hue="Model", join=False, dodge=0.3, markers=["o", "s"], palette="muted")
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.subplots_adjust(left=0.1, right=0.85, bottom=0.2, top=0.9)
plt.show()


# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2_corrected = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    cramers_v = np.sqrt(phi2_corrected / min((k - 1), (r - 1)))
    return cramers_v

# Extract real and GPT40 variable names
real_vars = [col for col in combo_file_c.columns if col.endswith("_real")]
gpt40_vars = [col.replace("_real", "_GPT40_adj") for col in real_vars]

# Function to extract the base question name
def extract_base_name(var_name):
    return var_name.split("_")[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(combo_file_c[real_var_i], combo_file_c[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": real_var_i,
                "Comparison": real_var_j,
                "Model": "Real",
                "CramersV": cramer_real
            })

# Calculate Cramér's V for each GPT40 variable against all real variables
for gpt40_var in gpt40_vars:
    base_name_i = extract_base_name(gpt40_var)
    for real_var_j in real_vars:
        if base_name_i != extract_base_name(real_var_j):
            cramer_gpt40 = calculate_cramers_v(combo_file_c[gpt40_var], combo_file_c[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": gpt40_var,
                "Comparison": real_var_j,
                "Model": "GPT40",
                "CramersV": cramer_gpt40
            })


# Extract real and GPT35 variable names
real_vars = [col for col in combo_file_c.columns if col.endswith("_real")]
gpt35_vars = [col.split("_")[-1] for col in real_vars]

# Function to extract the base question name
def extract_base_name(var_name):
    return var_name.split("_")[-1]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each GPT35 variable against all real variables
for gpt35_var in gpt35_vars:
    base_name_i = extract_base_name(gpt35_var)
    cramer_gpt35 = combo_file_c[base_name_i]
    results.append({
        "BaseName": base_name_i,
        "Variable": gpt35_var,
        "Comparison": cramer_gpt35,
        "Model": "GPT35"
    })

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results)

# Plot the results
fig, ax = plt.subplots(figsize=(8, 6))
for i, row in results_df.iterrows():
    base_name_i = row["BaseName"]
    ax.plot(row["Comparison"], label=base_name_i)
    ax.legend()

    

import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# Rename a column in results_40_turbo
results_40_turbo.rename(columns={"Q100_GPT35": "Q100_GPT40t"}, inplace=True)

# Convert results_40_turbo to a DataFrame
results_40_turbo = results_40_turbo.astype(object)

# Preprocess GPT-4 turbo results
results_40_turbo["Q41d_GPT40t"] = results_40_turbo["Q41d_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q41a_GPT40t"] = results_40_turbo["Q41a_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q6C_GPT40t"] = results_40_turbo["Q6C_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q9A_GPT40t"] = results_40_turbo["Q9A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q4A_GPT40t"] = results_40_turbo["Q4A_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q8_GPT40t"] = results_40_turbo["Q8_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q94_GPT40t"] = results_40_turbo["Q94_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q101_GPT40t"] = results_40_turbo["Q101_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q100_GPT40t"] = results_40_turbo["Q100_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)
results_40_turbo["Q1_GPT40t"] = results_40_turbo["Q1_GPT35"].str.replace(r"^[^:]+:\s*", "", regex=True, case=False)

# Combine datasets
combo_file_c = pd.concat([prompt_set, results_40_turbo], axis=1)

# Adjust GPT-4 turbo predictions
combo_file_c["Q41d_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q41d_GPT40t"] if row["Q41d_GPT40t"].lower() in row["Q41d_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q41a_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q41a_GPT40t"] if row["Q41a_GPT40t"].lower() in row["Q41a_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q6C_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q6C_GPT40t"] if row["Q6C_GPT40t"].lower() in row["Q6C_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q9A_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q9A_GPT40t"] if row["Q9A_GPT40t"].lower() in row["Q9A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q4A_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q4A_GPT40t"] if row["Q4A_GPT40t"].lower() in row["Q4A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q8_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q8_GPT40t"] if row["Q8_GPT40t"].lower() in row["Q8_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q94_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q94_GPT40t"] if row["Q94_GPT40t"].lower() in row["Q94_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q101_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q101_GPT40t"] if row["Q101_GPT40t"].lower() in row["Q101_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q100_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q100_GPT40t"] if row["Q100_GPT40t"].lower() in row["Q100_real"].str.lower().unique() else pd.NA, axis=1)
combo_file_c["Q1_GPT40t_adj"] = combo_file_c.apply(lambda row: row["Q1_GPT40t"] if row["Q1_GPT40t"].lower() in row["Q1_real"].str.lower().unique() else pd.NA, axis=1)

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape
    phi2_corrected = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    cramers_v = np.sqrt(phi2_corrected / min((k - 1), (r - 1)))
    return cramers_v

# Extract real and GPT40 turbo variable names
real_vars = [col for col in combo_file_c.columns if col.endswith("_real")]
gpt40t_vars = [col.replace("_real", "_GPT40t_adj") for col in real_vars]

# Function to extract the base question name
def extract_base_name(var_name):
    return var_name.split("_")[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(combo_file_c[real_var_i], combo_file_c[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": real_var_i,
                "Comparison": real_var_j,
                "Model": "Real",
                "CramersV": cramer_real
            })



import pandas as pd
import matplotlib.pyplot as plt

# Calculate Cramér's V for each GPT35 variable against all real variables
results = {}
for i, gpt35_var in enumerate(gpt35_vars):
    base_name_i = extract_base_name(gpt35_var)
    
    for j, real_var_j in enumerate(real_vars):
        if base_name_i != extract_base_name(real_var_j):
            cramer_gpt35 = calculate_cramers_v(combo_file_c[gpt35_var], combo_file_c[real_var_j])
            results[f"{gpt35_var}_vs_{real_var_j}"] = {
                "BaseName": base_name_i,
                "Variable": gpt35_var,
                "Comparison": real_var_j,
                "Model": "GPT4_turbo",
                "CramersV": cramer_gpt35
            }

# Combine all results into a single data frame
results_df = pd.DataFrame.from_dict(results, orient="index")

# Melt the data frame for plotting
results_melted = pd.melt(results_df, id_vars=["BaseName", "Variable", "Comparison", "Model"], value_name="CramersV")

# Filter out rows where Cramér's V is NA
results_melted = results_melted.dropna(subset=["CramersV"])

# Plot the results
plt.figure(figsize=(10, 6))
for base_name, group in results_melted.groupby("BaseName"):
    plt.subplot(2, 2, list(results_melted["BaseName"].unique()).index(base_name) + 1)
    for model, model_group in group.groupby("Model"):
        plt.scatter(model_group["CramersV"], model_group["Comparison"], label=model, marker=("o" if model == "GPT4_turbo" else "s"))
    plt.title(base_name)
    plt.xlabel("Cramér's V")
    plt.ylabel("Comparison Variables")
    plt.legend()
plt.suptitle("Cramér's V Correlations for Variables")
plt.tight_layout()
plt.show()



import pandas as pd
import numpy as np
from random import sample
import json

# fine tuning using new prompts:
prompt_set_finetuning = []
all_ids = prompt_set['ID'].unique()
for id_selected in all_ids:
    sub_sample_id = prompt_set.loc[prompt_set['ID'] == id_selected, ['Prompt', 'Response']]
    df_ft_w = pd.DataFrame({
        'ID': [id_selected] * 10,
        'Prompt': sub_sample_id['Prompt'].values.T,
        'Response': sub_sample_id['Response'].values.T
    })
    prompt_set_finetuning.append(df_ft_w)
prompt_set_ft = pd.concat(prompt_set_finetuning, ignore_index=True)

np.random.seed(123)
random_numbers = sample(list(prompt_set['ID'].unique()), 1000)
print(random_numbers)
prompt_set_ft_in = prompt_set_ft[prompt_set_ft['ID'].isin(random_numbers)]
prompt_set_ft_out = prompt_set_ft[~prompt_set_ft['ID'].isin(random_numbers)]

all_message_sets = []
for i in range(len(prompt_set_ft_in)):
    system_message = {"role": "system", "content": "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question."}
    user_message = {"role": "user", "content": prompt_set_ft_in.iloc[i]['Prompt']}
    assistant_message = {"role": "assistant", "content": prompt_set_ft_in.iloc[i]['Response']}
    message_set = {"messages": [system_message, user_message, assistant_message]}
    all_message_sets.append(message_set)

json_output = [json.dumps(x) for x in all_message_sets]

# Write each JSON string as a new line in a .jsonl file
with open("240607_FT_Sample_1000obs_SurveyPrompt.jsonl", "w") as f:
    f.write("\n".join(json_output))


import os
import openai
from tqdm import tqdm

# Set the OpenAI API key
openai.api_key = ''

prompt_set_exp = prompt_set[~prompt_set['ID'].isin(random_numbers)]

initial_forecasts_list_with_sys_msg_35_ft = []
for i in tqdm(range(1249, prompt_set_exp.shape[0] + 1)):  # dim(prompt_set)[1]
    sel_subject = prompt_set_exp.iloc[i - 1, :]
    subject_list = []
    for j in range(2, 12):
        system_message = "This survey is conducted with a Chat GPT agent to explore and analyze responses on various topical social issues. Your participation will help us understand the capabilities and insights of AI in addressing these important topics. Assuming you are the participant of the survey, please review the set of questions and answers and answer to the last question. Please make sure you provide no explanation and you answer using only predefined categories in the question."
        user_message = sel_subject[j]
        chat_outcome = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:pk-ox:absrvyprmpt1000:9XT2Xm61",  # "gpt-3.5-turbo-0613", "gpt-4", "gpt-3.5-turbo-1106""gpt-4o"
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=1
        )
        subject_list.append(chat_outcome.choices[0].message.content)
    subject_results = pd.DataFrame(subject_list, columns=["Q41d_GPT35", "Q41a_GPT35", "Q6C_GPT35", "Q9A_GPT35", "Q4A_GPT35", "Q8_GPT35", "Q94_GPT35", "Q101_GPT35", "Q100_real", "Q1_GPT35"])
    initial_forecasts_list_with_sys_msg_35_ft.append(subject_results)
    print(i)


import pandas as pd

# Combine initial forecasts list into a single DataFrame
results = pd.concat(initial_forecasts_list_with_sys_msg_35_ft, ignore_index=True)
results35ft = results.copy()
results35ft.columns = ["Q41d_GPT35", "Q41a_GPT35", "Q6C_GPT35", "Q9A_GPT35", "Q4A_GPT35", "Q8_GPT35", "Q94_GPT35", "Q101_GPT35", "Q100_real", "Q1_GPT35"]

# Remove leading text from columns
results35ft["Q41d_GPT35"] = results35ft["Q41d_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q41a_GPT35"] = results35ft["Q41a_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q6C_GPT35"] = results35ft["Q6C_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q9A_GPT35"] = results35ft["Q9A_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q4A_GPT35"] = results35ft["Q4A_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q8_GPT35"] = results35ft["Q8_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q94_GPT35"] = results35ft["Q94_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q101_GPT35"] = results35ft["Q101_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q100_GPT35"] = results35ft["Q100_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()
results35ft["Q1_GPT35"] = results35ft["Q1_GPT35"].str.replace(r'^[^:]+:\s*', '', regex=True).str.lower()

# Save the results35ft and initial_forecasts_list_with_sys_msg_35_ft to a pickle file
results35ft.to_pickle("240607_initial_forecasts_list_with_sys_msg_35_ft.pkl")
with open("240607_initial_forecasts_list_with_sys_msg_35_ft.pkl", "wb") as f:
    pickle.dump(initial_forecasts_list_with_sys_msg_35_ft, f)

# Combine prompt_set_exp and results35ft
combo_file = pd.concat([prompt_set_exp, results35ft], axis=1)

# Adjust GPT-35 responses to match real responses
combo_file["Q41d_GPT35_adj"] = combo_file.apply(lambda row: row["Q41d_GPT35"] if row["Q41d_GPT35"].lower() in combo_file["Q41d_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q41a_GPT35_adj"] = combo_file.apply(lambda row: row["Q41a_GPT35"] if row["Q41a_GPT35"].lower() in combo_file["Q41a_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q6C_GPT35_adj"] = combo_file.apply(lambda row: row["Q6C_GPT35"] if row["Q6C_GPT35"].lower() in combo_file["Q6C_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q9A_GPT35_adj"] = combo_file.apply(lambda row: row["Q9A_GPT35"] if row["Q9A_GPT35"].lower() in combo_file["Q9A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q4A_GPT35_adj"] = combo_file.apply(lambda row: row["Q4A_GPT35"] if row["Q4A_GPT35"].lower() in combo_file["Q4A_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q8_GPT35_adj"] = combo_file.apply(lambda row: row["Q8_GPT35"] if row["Q8_GPT35"].lower() in combo_file["Q8_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q94_GPT35_adj"] = combo_file.apply(lambda row: row["Q94_GPT35"] if row["Q94_GPT35"].lower() in combo_file["Q94_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q101_GPT35_adj"] = combo_file.apply(lambda row: row["Q101_GPT35"] if row["Q101_GPT35"].lower() in combo_file["Q101_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q100_GPT35_adj"] = combo_file.apply(lambda row: row["Q100_GPT35"] if row["Q100_GPT35"].lower() in combo_file["Q100_real"].str.lower().unique() else pd.NA, axis=1)
combo_file["Q1_GPT35_adj"] = combo_file.apply(lambda row: row["Q1_GPT35"] if row["Q1_GPT35"].lower() in combo_file["Q1_real"].str.lower().unique() else pd.NA, axis=1)

# Special case for Q101_GPT35_adj
combo_file.loc[0, "Q101_GPT35_adj"] = "coloured"


import pandas as pd
from scipy.stats import chi2_contingency

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

# Assume combo_file is a pandas DataFrame already loaded with the data

# Extract real and GPT35 variable names
real_vars = [col for col in combo_file.columns if col.endswith('_real')]
gpt35_vars = [col.replace('_real', '_GPT35_adj') for col in real_vars]

# Function to extract the base question name (e.g., "Q41d" from "Q41d_real")
def extract_base_name(var_name):
    return var_name.split('_')[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(combo_file[real_var_i], combo_file[real_var_j])
            results.append({
                'BaseName': base_name_i,
                'Variable': real_var_i,
                'Comparison': real_var_j,
                'Model': 'Real',
                'CramersV': cramer_real
            })

# Convert results list to DataFrame
results_df = pd.DataFrame(results)


import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

# Assume combo_file is a pandas DataFrame already loaded with the data

# Extract real and GPT35 variable names
real_vars = [col for col in combo_file.columns if col.endswith('_real')]
gpt35_vars = [col.replace('_real', '_GPT35_adj') for col in real_vars]

# Function to extract the base question name (e.g., "Q41d" from "Q41d_real")
def extract_base_name(var_name):
    return var_name.split('_')[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each GPT35 variable against all real variables
for gpt35_var in gpt35_vars:
    base_name_i = extract_base_name(gpt35_var)
    
    for real_var_j in real_vars:
        if extract_base_name(real_var_j) != base_name_i:
            cramer_gpt35 = calculate_cramers_v(combo_file[gpt35_var], combo_file[real_var_j])
            results.append({
                'BaseName': base_name_i,
                'Variable': gpt35_var,
                'Comparison': real_var_j,
                'Model': 'GPT35_FT',
                'CramersV': cramer_gpt35
            })

# Convert results list to DataFrame
results_df = pd.DataFrame(results)

# Melt the DataFrame for plotting
results_melted = pd.melt(results_df, id_vars=['BaseName', 'Variable', 'Comparison', 'Model'], value_vars=['CramersV'], var_name='CramersV')

# Filter out rows where Cramér's V is NaN
results_melted = results_melted.dropna(subset=['value'])

# Plot the results using seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=results_melted, x='value', y='Comparison', hue='Model', style='Model', s=100)
plt.title("Cramér's V Correlations for Variables")
plt.xlabel("Cramér's V")
plt.ylabel("Comparison Variables")
plt.tight_layout()
plt.show()



import pandas as pd
import numpy as np
import pickle

# Assume combo_file is already a pandas DataFrame containing your data

# Make a copy of combo_file for fine-tuned GPT3.5 results
combo_file_ft = combo_file.copy()

# Define breaks and labels for categorization
breaks = [-np.inf, 30, 45, 60, np.inf]
labels = ["18 to 30", "31 to 45", "46 to 60", "Above 60"]

# Cut Q1_real and Q1_GPT35_adj into categories
combo_file_ft['Q1_real_cat'] = pd.cut(pd.to_numeric(combo_file_ft['Q1_real'], errors='coerce'),
                                      bins=breaks, labels=labels, right=True, include_lowest=True)
combo_file_ft['Q1_GPT35_adj_cat'] = pd.cut(pd.to_numeric(combo_file_ft['Q1_GPT35_adj'], errors='coerce'),
                                           bins=breaks, labels=labels, right=True, include_lowest=True)

# Define question names and calculate hit ratios
q_names = ["Q41d", "Q41a", "Q6C", "Q9A", "Q8", "Q94", "Q101", "Q100", "Q1", "Q1_cat"]
ht_ft = [
    np.sum(combo_file_ft['Q41d_GPT35_adj'].str.lower() == combo_file_ft['Q41d_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q41d_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q41a_GPT35_adj'].str.lower() == combo_file_ft['Q41a_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q41a_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q6C_GPT35_adj'].str.lower() == combo_file_ft['Q6C_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q6C_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q9A_GPT35_adj'].str.lower() == combo_file_ft['Q9A_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q9A_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q8_GPT35_adj'].str.lower() == combo_file_ft['Q8_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q8_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q94_GPT35_adj'].str.lower() == combo_file_ft['Q94_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q94_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q101_GPT35_adj'].str.lower() == combo_file_ft['Q101_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q101_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q100_GPT35_adj'].str.lower() == combo_file_ft['Q100_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q100_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q1_GPT35_adj'].str.lower() == combo_file_ft['Q1_real'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q1_GPT35_adj'].dropna()),
    np.sum(combo_file_ft['Q1_GPT35_adj_cat'].str.lower() == combo_file_ft['Q1_real_cat'].str.lower(), na.rm=True) /
    len(combo_file_ft['Q1_GPT35_adj_cat'].dropna())
]

# Save combo_file_ft and combo_file using pickle
with open("240608_FineTunedResultsCleanFinalTable.pkl", "wb") as f1:
    pickle.dump(combo_file_ft, f1)

with open("240608_GPT35_GPT4o_ResultsCleanFinalTable.pkl", "wb") as f2:
    pickle.dump(combo_file, f2)


import pandas as pd
import numpy as np

# Assume combo_file is already a pandas DataFrame containing your data

# Define breaks and labels for categorization
breaks = [-np.inf, 30, 45, 60, np.inf]
labels = ["18 to 30", "31 to 45", "46 to 60", "Above 60"]

# Cut Q1_real, Q1_GPT35_adj, Q1_GPT40_adj into categories
combo_file['Q1_real_cat'] = pd.cut(pd.to_numeric(combo_file['Q1_real'], errors='coerce'),
                                   bins=breaks, labels=labels, right=True, include_lowest=True)
combo_file['Q1_GPT35_adj_cat'] = pd.cut(pd.to_numeric(combo_file['Q1_GPT35_adj'], errors='coerce'),
                                       bins=breaks, labels=labels, right=True, include_lowest=True)
combo_file['Q1_GPT40_adj_cat'] = pd.cut(pd.to_numeric(combo_file['Q1_GPT40_adj'], errors='coerce'),
                                       bins=breaks, labels=labels, right=True, include_lowest=True)

# Calculate hit ratios for GPT3.5
ht_gpt35 = [
    np.sum(combo_file['Q41d_GPT35_adj'].str.lower() == combo_file['Q41d_real'].str.lower(), na.rm=True) /
    len(combo_file['Q41d_GPT35_adj'].dropna()),
    np.sum(combo_file['Q41a_GPT35_adj'].str.lower() == combo_file['Q41a_real'].str.lower(), na.rm=True) /
    len(combo_file['Q41a_GPT35_adj'].dropna()),
    np.sum(combo_file['Q6C_GPT35_adj'].str.lower() == combo_file['Q6C_real'].str.lower(), na.rm=True) /
    len(combo_file['Q6C_GPT35_adj'].dropna()),
    np.sum(combo_file['Q9A_GPT35_adj'].str.lower() == combo_file['Q9A_real'].str.lower(), na.rm=True) /
    len(combo_file['Q9A_GPT35_adj'].dropna()),
    np.sum(combo_file['Q8_GPT35_adj'].str.lower() == combo_file['Q8_real'].str.lower(), na.rm=True) /
    len(combo_file['Q8_GPT35_adj'].dropna()),
    np.sum(combo_file['Q94_GPT35_adj'].str.lower() == combo_file['Q94_real'].str.lower(), na.rm=True) /
    len(combo_file['Q94_GPT35_adj'].dropna()),
    np.sum(combo_file['Q101_GPT35_adj'].str.lower() == combo_file['Q101_real'].str.lower(), na.rm=True) /
    len(combo_file['Q101_GPT35_adj'].dropna()),
    np.sum(combo_file['Q100_GPT35_adj'].str.lower() == combo_file['Q100_real'].str.lower(), na.rm=True) /
    len(combo_file['Q100_GPT35_adj'].dropna()),
    np.sum(combo_file['Q1_GPT35_adj'].str.lower() == combo_file['Q1_real'].str.lower(), na.rm=True) /
    len(combo_file['Q1_GPT35_adj'].dropna()),
    np.sum(combo_file['Q1_GPT35_adj_cat'].str.lower() == combo_file['Q1_real_cat'].str.lower(), na.rm=True) /
    len(combo_file['Q1_GPT35_adj_cat'].dropna())
]

# Calculate hit ratios for GPT4o
ht_gpt4o = [
    np.sum(combo_file['Q41d_GPT40_adj'].str.lower() == combo_file['Q41d_real'].str.lower(), na.rm=True) /
    len(combo_file['Q41d_GPT40_adj'].dropna()),
    np.sum(combo_file['Q41a_GPT40_adj'].str.lower() == combo_file['Q41a_real'].str.lower(), na.rm=True) /
    len(combo_file['Q41a_GPT40_adj'].dropna()),
    np.sum(combo_file['Q6C_GPT40_adj'].str.lower() == combo_file['Q6C_real'].str.lower(), na.rm=True) /
    len(combo_file['Q6C_GPT40_adj'].dropna()),
    np.sum(combo_file['Q9A_GPT40_adj'].str.lower() == combo_file['Q9A_real'].str.lower(), na.rm=True) /
    len(combo_file['Q9A_GPT40_adj'].dropna()),
    np.sum(combo_file['Q8_GPT40_adj'].str.lower() == combo_file['Q8_real'].str.lower(), na.rm=True) /
    len(combo_file['Q8_GPT40_adj'].dropna()),
    np.sum(combo_file['Q94_GPT40_adj'].str.lower() == combo_file['Q94_real'].str.lower(), na.rm=True) /
    len(combo_file['Q94_GPT40_adj'].dropna()),
    np.sum(combo_file['Q101_GPT40_adj'].str.lower() == combo_file['Q101_real'].str.lower(), na.rm=True) /
    len(combo_file['Q101_GPT40_adj'].dropna()),
    np.sum(combo_file['Q100_GPT40_adj'].str.lower() == combo_file['Q100_real'].str.lower(), na.rm=True) /
    len(combo_file['Q100_GPT40_adj'].dropna()),
    np.sum(combo_file['Q1_GPT40_adj'].str.lower() == combo_file['Q1_real'].str.lower(), na.rm=True) /
    len(combo_file['Q1_GPT40_adj'].dropna()),
    np.sum(combo_file['Q1_GPT40_adj_cat'].str.lower() == combo_file['Q1_real_cat'].str.lower(), na.rm=True) /
    len(combo_file['Q1_GPT40_adj_cat'].dropna())
]

# Save combo_file as combo_file_turbo using pickle
combo_file_turbo = combo_file.copy()
with open("240608_GPT40_Turbo_ResultsCleanFinalTable.pkl", "wb") as f:
    pickle.dump(combo_file_turbo, f)


import pandas as pd
import numpy as np

# Assume combo_file_turbo is already a pandas DataFrame containing your data

# Define breaks and labels for categorization
breaks = [-np.inf, 30, 45, 60, np.inf]
labels = ["18 to 30", "31 to 45", "46 to 60", "Above 60"]

# Cut Q1_real and Q1_GPT40t_adj into categories for combo_file_turbo
combo_file_turbo['Q1_real_cat'] = pd.cut(pd.to_numeric(combo_file_turbo['Q1_real'], errors='coerce'),
                                         bins=breaks, labels=labels, right=True, include_lowest=True)
combo_file_turbo['Q1_GPT40t_adj_cat'] = pd.cut(pd.to_numeric(combo_file_turbo['Q1_GPT40t_adj'], errors='coerce'),
                                               bins=breaks, labels=labels, right=True, include_lowest=True)

# Calculate hit ratios for GPT40t
ht_gpt40t = [
    np.sum(combo_file_turbo['Q41d_GPT40t_adj'].str.lower() == combo_file_turbo['Q41d_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q41d_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q41a_GPT40t_adj'].str.lower() == combo_file_turbo['Q41a_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q41a_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q6C_GPT40t_adj'].str.lower() == combo_file_turbo['Q6C_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q6C_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q9A_GPT40t_adj'].str.lower() == combo_file_turbo['Q9A_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q9A_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q8_GPT40t_adj'].str.lower() == combo_file_turbo['Q8_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q8_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q94_GPT40t_adj'].str.lower() == combo_file_turbo['Q94_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q94_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q101_GPT40t_adj'].str.lower() == combo_file_turbo['Q101_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q101_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q100_GPT40t_adj'].str.lower() == combo_file_turbo['Q100_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q100_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q1_GPT40t_adj'].str.lower() == combo_file_turbo['Q1_real'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q1_GPT40t_adj'].dropna()),
    np.sum(combo_file_turbo['Q1_GPT40t_adj_cat'].str.lower() == combo_file_turbo['Q1_real_cat'].str.lower(), na.rm=True) /
    len(combo_file_turbo['Q1_GPT40t_adj_cat'].dropna())
]

# Prepare accuracy table
ht_gpt35 = [0] * len(ht_gpt40t)  # Placeholder for ht_gpt35 (assumed to be similar structure)
ht_gpt4o = [0] * len(ht_gpt40t)  # Placeholder for ht_gpt4o (assumed to be similar structure)
ht_ft = [0] * len(ht_gpt40t)  # Placeholder for ht_ft (assumed to be similar structure)

accuracy_table = pd.DataFrame([ht_gpt35, ht_gpt4o, ht_gpt40t, ht_ft], columns=["TrustHealth", "ContactClinic", "WithoutMed", "FreeToSay", "Economy", "PolFamily", "Education", "Race", "Gender", "Age", "Age_cat"])
accuracy_table.index = ["GPT35", "GPT4o", "GPT40", "GPT35_FT"]
accuracy_table = accuracy_table.round(2)

# Define new_names dictionary for renaming rows
new_names = {
    "Q41d": "TrustHealth",
    "Q41a": "ContactClinic",
    "Q6C": "WithoutMed",
    "Q9A": "FreeToSay",
    "Q8": "PolFamily",
    "Q94": "Education",
    "Q101": "Race",
    "Q100": "Gender",
    "Q1": "Age",
    "Q1_cat": "Age_cat"
}

# Rename rows in accuracy_table
accuracy_table.rename(index=new_names, inplace=True)

# Print rounded accuracy table
print(accuracy_table)



import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# Assuming file_graph_turbo, file_graph_ft, and file_graph are already pandas DataFrames containing your data

def calculate_cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

# Extract real and GPT35 variable names
real_vars = [col for col in file_graph.columns if col.endswith("_real")]
gpt35_vars_turbo = [col.replace("_real", "_GPT40t_adj") for col in real_vars]  # GPT 4 turbo
gpt35_vars_ft = [col.replace("_real", "_GPT35_adj") for col in real_vars]  # GPT 3.5 FT
gpt35_vars_non_ft = [col.replace("_real", "_GPT35_adj") for col in real_vars]  # GPT 3.5 Non-FT
gpt40_vars_non_ft = [col.replace("_real", "_GPT40_adj") for col in real_vars]  # GPT 4.o Non-FT

# Function to extract the base question name (e.g., "Q41d" from "Q41d_real")
def extract_base_name(var_name):
    return var_name.split("_")[0]

# Initialize an empty list to store the results
results = []

# Calculate Cramér's V for each real variable against all other real variables
for i, real_var_i in enumerate(real_vars):
    base_name_i = extract_base_name(real_var_i)
    
    for j, real_var_j in enumerate(real_vars):
        if i != j:
            cramer_real = calculate_cramers_v(file_graph[real_var_i], file_graph[real_var_j])
            results.append({
                "BaseName": base_name_i,
                "Variable": real_var_i,
                "Comparison": real_var_j,
                "Model": "Real",
                "CramersV": cramer_real
            })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display the results DataFrame
print(results_df)



import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming results_df is the DataFrame containing the results from the previous calculation

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

# Assuming results_df is already created in the previous step

# Melt the data frame for visualization (similar to gather in R)
results_melted = results_df.melt(id_vars=["BaseName", "Variable", "Comparison", "Model"], value_vars=["CramersV"], var_name="CramersV")

# Filter out rows where Cramér's V is NaN
results_melted = results_melted.dropna(subset=["CramersV"])

# Rename BaseName and Comparison columns
new_names1 = {
    "Q41d": "TrustHealth",
    "Q41a": "ContactClinic",
    "Q6C": "WithoutMed",
    "Q9A": "FreeToSay",
    "Q4A": "Economy",
    "Q8": "PolFamily",
    "Q94": "Education",
    "Q101": "Race",
    "Q100": "Gender",
    "Q1": "Age"
}

new_names2 = {
    "Q41d_real": "TrustHealth",
    "Q41a_real": "ContactClinic",
    "Q6C_real": "WithoutMed",
    "Q9A_real": "FreeToSay",
    "Q4A_real": "Economy",
    "Q8_real": "PolFamily",
    "Q94_real": "Education",
    "Q101_real": "Race",
    "Q100_real": "Gender",
    "Q1_real": "Age"
}

results_melted["BaseName"] = results_melted["BaseName"].map(new_names1)
results_melted["Comparison"] = results_melted["Comparison"].map(new_names2)

# Plot the results using seaborn
plt.figure(figsize=(12, 8))
sns.scatterplot(data=results_melted, x="CramersV", y="Comparison", hue="Model", style="Model", s=100)
plt.title("Cramér's V Correlations for Variables")
plt.xlabel("Cramér's V")
plt.ylabel("Comparison Variables")
plt.legend(title="Model", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

