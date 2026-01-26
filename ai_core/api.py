
import json
import re
from .main import call_llm, safe_execute
from .memory.memory import save_memory

pending_action = None


def extract_json(text):
    """
    Extract first JSON object from text safely
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    return match.group(0)

def process_request(user_input, user_level="admin"):
    global pending_action

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

    # Safe actions
    result = safe_execute(intent_data, user_level)
    return {"status": "ok", "result": result}

def rule_based_intent(user_input):
    text = user_input.lower().strip()

    if "create file" in text:
        return {"intent": "CREATE_FILE", "path": "crisbee_test.txt"}

    if "delete file" in text:
        return {"intent": "DELETE_FILE", "path": "crisbee_test.txt"}

    if "file" in text or "files" in text:
        return {"intent": "LIST_FILES", "path": None}

    if "system" in text or "info" in text:
        return {"intent": "SYSTEM_INFO", "path": None}

    return {"intent": "UNKNOWN", "path": None}

