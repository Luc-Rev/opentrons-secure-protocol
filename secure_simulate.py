# secure_simulate.py
import os
from getpass import getpass
from auth_utils import load_users, verify_user
from opentrons import simulate

PROTOCOL = "mon_protocole.py"

if __name__ == "__main__":
    user = input("User: ").strip()
    pwd = getpass("Password: ")
    users = load_users()
    if not verify_user(users, user, pwd):
        raise SystemExit("⛔ Auth failed")

    os.environ["OT_AUTH"] = "OK"
    os.environ["OT_USER"] = user

    with open(PROTOCOL, "r", encoding="utf-8") as f:
        runlog, _ = simulate.simulate(f)

    for c in runlog:
        msg = c.get("payload", {}).get("text")
        if msg:
            print(msg)