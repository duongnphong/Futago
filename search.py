import os
import re
from datetime import date, datetime, timedelta

import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from ultis import load_faiss_and_metadata, search_index

load_dotenv()
# SYSTEM_PROMPT = open("./data/prompt.txt", "r").read()
MODEL_NAME = "gemini-1.5-flash-latest"
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

instructions = open("./data/prompt.txt", "r").read()


# Fine-tune on date, day, time
def prompt_ehancement_v1(query, today_str=None):
    if today_str is None:
        today = datetime.today()
    else:
        today = datetime.strptime(today_str, "%Y-%m-%d")
    replacements = {
        r"\b2 days ago\b": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        r"\byesterday\b": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        r"\btoday\b": today.strftime("%Y-%m-%d"),
        r"\btomorrow\b": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
    }

    for pattern, date_str in replacements.items():
        query = re.sub(pattern, date_str, query, flags=re.IGNORECASE)

    return query


# Fine-tune on query context
def prompt_enhancement_v2(query, chat_history=None):
    prompt = (
        instructions
        + f"""given this history:
    {chat_history}
    and this query:
    {query}
    Refine the query to be more specific and relevant to the context.
    If there is no history, just return the query.
    No need to change word choice, just make it more specific.
    ONLY RETURN THE REFINE QUERY, DO NOT RETURN ANYTHING ELSE.
    """
    )
    try:
        enhance_query = model.generate_content(prompt)
        return enhance_query.text
    except Exception as e:
        return f"An error with Gemini API: {e}"


def final_prompt(query, chat_history=None):
    query = prompt_ehancement_v1(query)
    query = prompt_enhancement_v2(query, chat_history)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index, metadata = load_faiss_and_metadata()
    results = search_index(query, model, index, metadata, k=5)
    # Remove duplicates by content
    seen = set()
    unique_results = []
    for r in results:
        content = r["content"].strip()
        if content not in seen:
            seen.add(content)
            unique_results.append(r)

    results = unique_results
    # for r in results:
    #     print(f"{r['metadata']['date']} - {r['metadata']['section']}")
    #     print(r["content"])
    today_str = date.today().strftime("%Y-%m-%d")
    context = "\n\n".join(
        [
            f"[{c['metadata']['date']} - {c['metadata']['section']}]\n{c['content']}"
            for c in results
        ]
    )

    prompt = (
        instructions
        + f"""
You will have acces to today date which is {today_str}.
You will also have access to conversation history.
{chat_history}
## Context to answer the question.
{context}
## Question:
{query}"""
    )
    return prompt


# if __name__ == "__main__":
#     # loop
#     while True:
#         query = input("You: ")
#         print(final_prompt(query))
#         print("-" * 50)
