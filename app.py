from flask import Flask, jsonify, render_template, request

from gemini import ask_gemini, ask_llama

app = Flask(__name__)

MODEL = ask_gemini


@app.route("/")
def index():
    return render_template("index.html")  # Looks in templates/


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    response = MODEL(user_prompt)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
