import json
import os
from datetime import datetime

USER_FILE = "users.json"
AUDIT_LOG = "audit.log"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def log_audit(action, target_user, actor="system"):
    """Write an entry into the audit log with timestamp, actor, and action."""
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {actor} | {action} | {target_user}\n")

if __name__ == "__main__":
    username = input("Enter the username to remove: ").strip()
    users = load_users()

    if username in users:
        confirm = input(f"⚠️ Do you really want to remove {username}? (y/n): ").lower()
        if confirm == "y":
            del users[username]
            save_users(users)
            print(f"✅ User {username} has been removed.")
            log_audit("REMOVE_USER", username, actor="admin")  # you can replace "admin" dynamically
        else:
            print("❌ Operation cancelled.")
    else:
        print("User not found.")