from flask import Flask, jsonify, render_template, request

from gemini import ask_gemini, ask_llama

app = Flask(__name__)

MODEL = ask_llama
MAX_HISTORY_TURNS = 4
chat_history = []  # Store history globally (for now)


@app.route("/")
def index():
    return render_template("index.html")  # Looks in templates/


@app.route("/ask", methods=["POST"])
def ask():
    global chat_history  # Needed to modify the global variable
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    response = MODEL(user_prompt, chat_history)
    chat_history.append({"user": user_prompt, "assistant": response})
    if len(chat_history) > MAX_HISTORY_TURNS:
        chat_history = chat_history[-MAX_HISTORY_TURNS:]
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
