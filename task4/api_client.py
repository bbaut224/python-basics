import requests

def fetch_user(user_id: int):
    r = requests.get(f"https://example.com/users/{user_id}")
    return r.json()
