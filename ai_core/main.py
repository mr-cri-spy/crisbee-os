from .memory.memory import init_db, save_memory
from .permissions.permissions import check_permission
import subprocess
import json
import os

MODEL = "qwen2.5:7b-instruct"

SYSTEM_PROMPT = """
You are Crisbee OS AI Core.

You MUST respond in VALID JSON ONLY.
Do not include explanations, markdown, or extra text.

Allowed intents:
- LIST_FILES
- SYSTEM_INFO
- UNKNOWN

Rules:
- If unsure, use intent UNKNOWN
- path must be null or a string

JSON format ONLY:
{
  "intent": "LIST_FILES",
  "path": null
}
"""



CRISBEE_ROOT = os.path.join(os.path.expanduser("~"), "CrisbeeWorkspace")
os.makedirs(CRISBEE_ROOT, exist_ok=True)





SANDBOX_PATHS = [
    os.path.expanduser("~"),
    os.path.join(os.path.expanduser("~"), "CrisbeeWorkspace")
]

os.makedirs(SANDBOX_PATHS[1], exist_ok=True)





def call_llm(user_input):
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )

    raw_output = result.stdout.strip()

    # DEBUG (always visible in terminal)
    print("\n--- RAW LLM OUTPUT ---")
    print(raw_output)
    print("--- END RAW OUTPUT ---\n")


    return raw_output


def safe_execute(intent_data, user_level="admin"):
    intent = intent_data.get("intent")
    path = intent_data.get("path")

    if not intent or intent == "UNKNOWN":
        return "I didn't understand that action."

    if not check_permission(intent, user_level):
        return "Permission denied for this action."

    elif intent == "LIST_FILES":
        return os.listdir(CRISBEE_ROOT)



    elif intent == "SYSTEM_INFO":
        return {
            "user": os.getlogin(),
            "cwd": os.getcwd()
        }

    elif intent == "CREATE_FILE":
        if not path:
            return "No file path provided."

        full_path = os.path.join(CRISBEE_ROOT, path)

        with open(full_path, "w") as f:
            f.write("Created by Crisbee OS")

        return f"File '{path}' created inside CrisbeeWorkspace."




    elif intent == "DELETE_FILE":
        if not path:
            return "No file path provided."

        full_path = os.path.join(CRISBEE_ROOT, path)

        if os.path.exists(full_path):
            os.remove(full_path)
            return f"File '{path}' deleted from CrisbeeWorkspace."

        return "File not found in CrisbeeWorkspace."



    elif intent == "LAUNCH_APP":
        if not path:
            return "No application specified."

        subprocess.Popen([path])
        return f"Launching {path}"

    else:
        return "Action not supported."




def is_path_allowed(path):
    if not path:
        return False
    abs_path = os.path.abspath(path)

    for sandbox in SANDBOX_PATHS:
        if abs_path.startswith(os.path.abspath(sandbox)):
            return True

    return False


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

