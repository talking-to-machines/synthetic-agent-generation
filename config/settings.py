import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env.

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_HOME = os.environ.get("HF_HOME")
ANTROPIC_API_KEY = os.environ.get("ANTROPIC_API_KEY")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
GROK_API_KEY = os.environ.get("GROK_API_KEY")
