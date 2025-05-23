import os

import google.generativeai as genai
import requests
from dotenv import load_dotenv

from search import final_prompt

load_dotenv()
# SYSTEM_PROMPT = open("./data/prompt.txt", "r").read()
MODEL_NAME = "gemini-1.5-flash-latest"
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def ask_gemini(prompt_text):
    prompt = final_prompt(prompt_text)
    # print("-" * 100)
    # print("FINAL PROMPT AFTER COMBINING WITH RETRIVED RAG:")
    # print(prompt)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error with Gemini API: {e}"


def ask_llama(prompt_text):
    prompt = final_prompt(prompt_text)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b-instruct",
                "prompt": prompt,
                "stream": False,
            },
        )
        return response.json()["response"]
    except Exception as e:
        return f"An error with Ollama API: {e}"


# if __name__ == "__main__":
#     # asking in loop
#     while True:
#         prompt_text = input("You: ")
#         response = ask_gemini(prompt_text)
#         # print("-" * 100)
#         print("Tom:", response)
