import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from main import ask_deepseek, ask_gemini

# from ollama import ask_deepseek

# Load secrets
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  # Looks in templates/


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    response = ask_gemini(user_prompt)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
