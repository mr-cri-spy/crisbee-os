PERMISSIONS = {
    "LIST_FILES": "read",
    "SYSTEM_INFO": "read",
    "CREATE_FILE": "write",
    "DELETE_FILE": "admin",
}

def check_permission(intent, user_level="read"):
    # UNKNOWN or no action → always allow (no execution)
    if intent not in PERMISSIONS:
        return True

    required = PERMISSIONS[intent]

    levels = ["read", "write", "admin"]

    return levels.index(user_level) >= levels.index(required)

