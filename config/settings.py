import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env.

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_HOME = os.environ.get("HF_HOME")
