import os
import json

PROFILE_PATH = os.path.join(
    os.path.expanduser("~"),
    "CrisbeeWorkspace",
    "profile.json"
)

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        profile = {"user": os.getlogin(), "role": "admin"}
        save_profile(profile)
        return profile
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f)