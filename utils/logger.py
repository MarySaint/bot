import requests
import os

def log_action(user, action,level):
    URL = os.getenv("LOGGER")
    try:
        requests.post(f"{URL}/log/", json={"user": user, "action": action,"level":level})
    except:
        pass
