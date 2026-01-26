
import json
import re
from .main import call_llm, safe_execute
from .memory.memory import save_memory

def extract_json(text):
    """
    Extract first JSON object from text safely
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    return match.group(0)

def process_request(user_input, user_level="read"):
    raw = call_llm(user_input)

    json_text = extract_json(raw)
    if not json_text:
        return {
            "status": "error",
            "result": "AI did not return valid JSON"
        }

    try:
        intent_data = json.loads(json_text)
        save_memory(user_input, intent_data.get("intent"))
        result = safe_execute(intent_data, user_level)

        return {
            "status": "ok",
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "result": f"JSON parse error: {e}"
        }

