import re
from datetime import date, datetime, timedelta

from sentence_transformers import SentenceTransformer

from ultis import load_faiss_and_metadata, search_index

instructions = open("./data/prompt.txt", "r").read()


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


def final_prompt(query):
    query = prompt_ehancement_v1(query)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index, metadata = load_faiss_and_metadata()
    results = search_index(query, model, index, metadata, k=5)
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
## Context:
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
