import os
import re
from datetime import date, timedelta

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-flash-latest"
DIARY_DIR = "diary"
WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

with open("./data/prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().strip()


def parse_relative_date(prompt_text):
    prompt_lower = prompt_text.lower()
    today = date.today()

    if "today" in prompt_lower:
        return today

    if "yesterday" in prompt_lower:
        return today - timedelta(days=1)

    if "this week" in prompt_lower:
        monday = today - timedelta(days=today.weekday())
        return (monday, today)

    match = re.search(r"(\d+)\s+days?\s+ago", prompt_lower)
    if match:
        return today - timedelta(days=int(match.group(1)))

    # Match "last Monday" or "on Tuesday"
    for weekday_name, weekday_index in WEEKDAYS.items():
        if f"last {weekday_name}" in prompt_lower:
            days_ago = (today.weekday() - weekday_index + 7) % 7 + 7
            return today - timedelta(days=days_ago)
        elif (
            f"on {weekday_name}" in prompt_lower
            or f"this {weekday_name}" in prompt_lower
        ):
            days_ago = (today.weekday() - weekday_index + 7) % 7
            return today - timedelta(days=days_ago)

    return None


def read_diary_entries_in_range(start_date, end_date):
    entries = []
    delta = timedelta(days=1)

    current = start_date
    while current <= end_date:
        file_path = f"diary/{current.strftime('%Y%m%d')}.md"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                entries.append(f"[{current.strftime('%Y-%m-%d')}]\n{f.read().strip()}")
        current += delta

    return "\n\n".join(entries) if entries else None


def read_diary_entry(date_obj):
    """Reads diary entry for the given date."""
    date_str = date_obj.strftime("%Y%m%d")
    file_path = os.path.join(DIARY_DIR, f"{date_str}.md")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return None


def parse_relative_date_range(prompt_text):
    prompt_lower = prompt_text.lower()
    today = date.today()

    if "this week" in prompt_lower:
        monday = today - timedelta(days=today.weekday())  # Monday of this week
        return (monday, today)

    return None  # Not a date range


def ask_gemini(prompt_text):
    today_str = date.today().strftime("%Y-%m-%d")
    final_prompt = f"{SYSTEM_PROMPT}\n\nToday is {today_str}.\n"

    # Date range support
    date_range = parse_relative_date_range(prompt_text)
    if date_range:
        start, end = date_range
        combined_entries = read_diary_entries_in_range(start, end)
        if combined_entries:
            final_prompt += f"\nHere are your diary entries from {start} to {end}:\n{combined_entries}\n"
        else:
            final_prompt += f"\nNo diary entries found from {start} to {end}.\n"
    else:
        # Fallback to single day
        target_date = parse_relative_date(prompt_text)
        if target_date:
            diary_entry = read_diary_entry(target_date)
            if diary_entry:
                final_prompt += f"\nDiary entry for {target_date}:\n{diary_entry}\n"
            else:
                final_prompt += f"\nNo diary entry for {target_date}.\n"

    final_prompt += f"\nUser prompt: {prompt_text}"

    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the Gemini API: {e}"


def main():
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == "exit":
            break
        if not user_prompt:
            continue

        gemini_response = ask_gemini(user_prompt)
        print(f"Gemini: {gemini_response}")


if __name__ == "__main__":
    main()
