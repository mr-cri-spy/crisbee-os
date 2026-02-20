import os
import subprocess

CRISBEE_ROOT = os.path.join(
    os.path.expanduser("~"),
    "CrisbeeWorkspace"
)
os.makedirs(CRISBEE_ROOT, exist_ok=True)

PERMISSIONS = {
    "LIST_FILES": "user",
    "SYSTEM_INFO": "user",
    "HELP": "user",
    "WHOAMI": "user",
    "CREATE_FILE": "admin",
    "DELETE_FILE": "admin",
    "LAUNCH_APP": "admin"
}

def check_permission(intent, role):
    required = PERMISSIONS.get(intent, "admin")
    if role == "admin":
        return True
    return required == "user"

def safe_execute(intent_data, role):
    if not intent_data:
        return "No action to execute."

    intent = intent_data.get("intent")
    path = intent_data.get("path")
    
    

    if not check_permission(intent, role):
        return "This action requires admin privileges."

    if intent == "HELP":
        return (
            "I can manage files inside CrisbeeWorkspace, "
            "launch approved applications, and answer system queries."
        )

    elif intent == "LIST_FILES":
        return str(os.listdir(CRISBEE_ROOT))

    elif intent == "SYSTEM_INFO":
        return f"User: {os.getlogin()} | CWD: {os.getcwd()}"

    elif intent == "CREATE_FILE":
        full_path = os.path.join(CRISBEE_ROOT, path)
        with open(full_path, "w") as f:
            f.write("Created by Crisbee OS")
        return f"File '{path}' created."

    elif intent == "DELETE_FILE":
        full_path = os.path.join(CRISBEE_ROOT, path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return f"File '{path}' deleted."
        return "File not found."

    elif intent == "LAUNCH_APP":
        subprocess.Popen([path])
        return f"Launching {path}"
    
    elif intent == "SHOW_AUDIT":
        import sqlite3
        from .memory.memory import DB_PATH

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user, role, intent, target, status, timestamp FROM audit_log ORDER BY id DESC LIMIT 10")
        rows = c.fetchall()
        conn.close()

        return str(rows)
    
    
    return "Action not supported."

    log_audit(user, role, intent, intent_data.get("path"), "DENIED")
