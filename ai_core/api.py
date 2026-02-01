pending_action = None

import json
import re
from .main import call_llm, safe_execute
from .memory.memory import save_memory
from .memory.profile import load_profile

from .main import safe_execute
from .memory.memory import save_memory, most_frequent_targets





def extract_json(text):
    """
    Extract first JSON object from text safely
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    return match.group(0)



def rule_based_intent(user_input):
    text = user_input.lower().strip()

    # Help
    if "help" in text or "what can you do" in text:
        return {"intent": "HELP", "path": None}

    # File operations
    if "create file" in text:
        parts = text.split()
        if len(parts) >= 3:
            return {"intent": "CREATE_FILE", "path": parts[-1]}

    if "delete file" in text:
        parts = text.split()
        if len(parts) >= 3:
            return {"intent": "DELETE_FILE", "path": parts[-1]}

    if "file" in text or "files" in text:
        return {"intent": "LIST_FILES", "path": None}

    # App launch
    if text.startswith("open ") or text.startswith("launch "):
        app = text.split(maxsplit=1)[1]
        return {"intent": "LAUNCH_APP", "path": app}

    # Identity
    if "who am i" in text:
        return {"intent": "WHOAMI", "path": None}

    return {"intent": "UNKNOWN", "path": None}






def process_request(user_input, user_level="read"):
    global pending_action
    profile = load_profile()
    current_user = profile["user"]
    

    text = user_input.lower().strip()

    # Confirmation step
    if pending_action:
        if text in ["yes", "confirm", "ok"]:
            result = safe_execute(pending_action, user_level)
            pending_action = None
            return {"status": "ok", "result": result}
        else:
            pending_action = None
            return {"status": "ok", "result": "Action cancelled."}

    # PURE rule-based intent (v0.5)
    intent_data = rule_based_intent(user_input)

    # Guard UNKNOWN immediately
    if intent_data["intent"] == "UNKNOWN":
        return {"status": "ok", "result": "I didn't understand that action."}

    # Require confirmation for dangerous actions
    if intent_data["intent"] in ["CREATE_FILE", "DELETE_FILE"]:
        pending_action = intent_data
        return {
            "status": "ok",
            "result": "Are you sure you want to perform this action? Type yes to confirm."
        }
    
    if "who am i" in text:
        return {"intent": "WHOAMI", "path": None}
    elif intent == "WHOAMI":
        return f"You are logged in as {current_user}"



    # Safe actions
    result = safe_execute(intent_data, user_level)
    return {"status": "ok", "result": result}




