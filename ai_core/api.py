from .main import safe_execute
from .memory.memory import save_memory, init_db, log_audit
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

    if "show audit" in text:
        return {"intent": "SHOW_AUDIT", "path": None}

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

    # ----- Confirmation Handling -----
    if pending_action is not None:
        action = pending_action
        pending_action = None

        if user_input.lower() in ["yes", "confirm"]:
            result = safe_execute(action, role)

            save_memory(user, action["intent"], action.get("path"))
            log_audit(user, role, action["intent"], action.get("path"), "ALLOWED")

            return {"result": result}
        else:
            log_audit(user, role, action["intent"], action.get("path"), "CANCELLED")
            return {"result": "Action cancelled."}

    # ----- WHOAMI -----
    if intent == "WHOAMI":
        return {"result": f"You are logged in as {user} with role {role}"}

    # ----- UNKNOWN -----
    if intent == "UNKNOWN":
        return {"result": "I didn't understand that action. Type help."}

    # ----- Destructive Actions -----
    if intent in ["CREATE_FILE", "DELETE_FILE"]:
        pending_action = intent_data
        return {"result": "Are you sure? Type yes to confirm."}

    # ----- Normal Execution -----
    result = safe_execute(intent_data, role)

    # ----- Audit Logging -----
    if result == "This action requires admin privileges.":
        log_audit(user, role, intent, intent_data.get("path"), "DENIED")
    else:
        log_audit(user, role, intent, intent_data.get("path"), "ALLOWED")

    return {"result": result}