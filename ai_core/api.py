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








def process_request(user_input):
    global pending_action

    # Always normalize input
    text = user_input.strip().lower()

    # Resolve intent once
    intent_data = rule_based_intent(text)
    intent = intent_data.get("intent")
    path = intent_data.get("path")

    # Handle confirmation state
    if pending_action:
        if text in ["yes", "confirm", "ok"]:
            result = safe_execute(pending_action)
            pending_action = None
            return {"result": result}
        else:
            pending_action = None
            return {"result": "Action cancelled."}

    # WHOAMI handled here (no execution)
    if intent == "WHOAMI":
        profile = load_profile()
        return {"result": f"You are logged in as {profile['user']}"}

    # Unknown intent
    if intent == "UNKNOWN":
        return {"result": "I didn't understand that action. Type help to see what I support."}

    # Confirmation required for destructive actions
    if intent in ["CREATE_FILE", "DELETE_FILE"]:
        pending_action = intent_data
        return {"result": "Are you sure you want to perform this action? Type yes to confirm."}

    # Normal execution
    result = safe_execute(intent_data)
    return {"result": result}

