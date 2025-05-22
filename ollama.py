from datetime import date

import requests


def ask_deepseek(prompt_text):
    today_str = date.today().strftime("%Y-%m-%d")
    full_prompt = f"Today is {today_str}.\n{prompt_text}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:7b-instruct",
            "prompt": full_prompt,
            "stream": False,
        },
    )
    result = response.json()
    # print(result)  # debug

    if "response" in result:
        return result["response"]
    return "No response from DeepSeek."
