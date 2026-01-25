import subprocess
import json
import os

MODEL = "qwen2.5:7b-instruct"

SYSTEM_PROMPT = """
You are Crisbee OS AI Core.
Your job is to classify user intent and respond ONLY in JSON.

Allowed intents:
- LIST_FILES
- READ_FILE
- SYSTEM_INFO
- UNKNOWN

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

def safe_execute(intent_data):
    intent = intent_data.get("intent")
    path = intent_data.get("path")

    if intent == "LIST_FILES":
        if path is None:
            path = os.path.expanduser("~")
        return os.listdir(path)

    elif intent == "SYSTEM_INFO":
        return {
            "cwd": os.getcwd(),
            "user": os.getlogin()
        }

    else:
        return "Action not allowed or unknown."

def main():
    print("🐝 Crisbee OS AI Core v0.1")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You > ")

        if user_input.lower() == "exit":
            break

        raw = call_llm(user_input)

        try:
            intent_data = json.loads(raw)
            result = safe_execute(intent_data)
            print("Crisbee >", result)

        except Exception as e:
            print("Crisbee > Error understanding request")

if __name__ == "__main__":
    main()
