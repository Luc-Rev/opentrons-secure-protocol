from getpass import getpass
from auth_utils import load_users, save_users, create_user

if __name__ == "__main__":
    username = input("New user: ").strip()
    if not username:
        raise SystemExit("user name empty.")
    pwd1 = getpass("passwords: ")
    pwd2 = getpass("Confirm password: ")
    if pwd1 != pwd2:
        raise SystemExit("The passwords do not match.")
    users = load_users()
    if username in users:
        raise SystemExit("This user already exists.")
    users = create_user(users, username, pwd1)
    save_users(users)
    print(f"OK: user '{username}' add.")