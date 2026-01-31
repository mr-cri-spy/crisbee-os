import os
import json

PROFILE_PATH = os.path.join(os.path.expanduser("~"), "CrisbeeWorkspace", "profile.json")

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return {"user": os.getlogin(), "role": "admin"}
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f)
