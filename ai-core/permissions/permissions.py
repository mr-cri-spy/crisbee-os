PERMISSIONS = {
    "LIST_FILES": "read",
    "READ_FILE": "read",
    "SYSTEM_INFO": "read",
    "DELETE_FILE": "admin",
    "INSTALL_APP": "admin"
}

def check_permission(intent, user_level="read"):
    required = PERMISSIONS.get(intent, "none")

    levels = ["read", "write", "admin"]

    return levels.index(user_level) >= levels.index(required)

