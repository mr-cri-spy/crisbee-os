import subprocess
import json
import os

from memory.memory import init_db, save_memory
from permissions.permissions import check_permission

MODEL = "qwen2.5:7b-instruct"

SYSTEM_PROMPT = """
You are Crisbee OS AI Core.
Classify the user's intent and respond ONLY in JSON.

Allowed intents:
- LIST_FILES
- READ_FILE
- SYSTEM_INFO

Rules:
- Do NOT explain
- Do NOT execute commands
- Output valid JSON only

JSON format:
{
  "intent": "<INTENT>",
  "path": "<path or null>"
}
"""

def call_llm(user_input):
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()

def safe_execute(intent_data, user_level="read"):
    intent = intent_data.get("intent")
    path = intent_data.get("path")

    # Permission check
    if not check_permission(intent, user_level):
        return "Permission denied for this action."

    if intent == "LIST_FILES":
        if path is None:
            path = os.path.expanduser("~")
        return os.listdir(path)

    elif intent == "SYSTEM_INFO":
        return {
            "user": os.getlogin(),
            "cwd": os.getcwd()
        }

    else:
        return "⚠ Unknown or unsupported action."

def main():
    init_db()
    print("Crisbee OS AI Core v0.2")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You > ")

        if user_input.lower() == "exit":
            break

        raw = call_llm(user_input)

        try:
            intent_data = json.loads(raw)

            # Save memory
            save_memory(user_input, intent_data.get("intent"))

            result = safe_execute(intent_data)
            print("Crisbee >", result)

        except Exception:
            print("Crisbee > Error understanding request")

if __name__ == "__main__":
    main()

