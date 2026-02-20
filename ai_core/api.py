from .main import safe_execute
from .memory.memory import save_memory, init_db
from .memory.profile import load_profile

pending_action = None

init_db()

def rule_based_intent(user_input):
    text = user_input.lower().strip()

    if "help" in text:
        return {"intent": "HELP", "path": None}

    if "who am i" in text:
        return {"intent": "WHOAMI", "path": None}

    if "create file" in text:
        return {"intent": "CREATE_FILE", "path": text.split()[-1]}

    if "delete file" in text:
        return {"intent": "DELETE_FILE", "path": text.split()[-1]}

    if "show files" in text or "list files" in text:
        return {"intent": "LIST_FILES", "path": None}

    if text.startswith("open "):
        return {"intent": "LAUNCH_APP", "path": text.split(maxsplit=1)[1]}

    return {"intent": "UNKNOWN", "path": None}

def process_request(user_input):
    global pending_action

    profile = load_profile()
    role = profile["role"]
    user = profile["user"]

    intent_data = rule_based_intent(user_input)
    intent = intent_data.get("intent")

    if pending_action:
        if user_input.lower() in ["yes", "confirm"]:
            result = safe_execute(pending_action, role)
            save_memory(user, pending_action["intent"], pending_action["path"])
            pending_action = None
            return {"result": result}
        else:
            pending_action = None
            return {"result": "Action cancelled."}

    if intent == "WHOAMI":
        return {"result": f"You are logged in as {user} with role {role}"}

    if intent == "UNKNOWN":
        return {"result": "I didn't understand that action. Type help."}

    if intent in ["CREATE_FILE", "DELETE_FILE"]:
        pending_action = intent_data
        return {"result": "Are you sure? Type yes to confirm."}

    result = safe_execute(intent_data, role)
    return {"result": result}