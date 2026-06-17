import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables from .env file (for LangSmith)
load_dotenv()

# We use Ollama for local, offline inference.
# Make sure you have Ollama installed and have pulled the model, e.g., `ollama pull llama3`
model = ChatOllama(
    model="llama3",
    temperature=0.1,
)
