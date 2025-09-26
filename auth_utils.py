# auth_utils.py
import json, os, hashlib, hmac, secrets
from typing import Dict

USERS_FILE = "users.json"

def _pbkdf2(password: str, salt: bytes, iters: int = 200_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)

def create_user(users: Dict[str, dict], username: str, password: str) -> Dict[str, dict]:
    salt = secrets.token_bytes(16)
    pwd_hash = _pbkdf2(password, salt)
    users[username] = {"salt": salt.hex(), "hash": pwd_hash.hex()}
    return users

def verify_user(users: Dict[str, dict], username: str, password: str) -> bool:
    rec = users.get(username)
    if not rec: return False
    salt = bytes.fromhex(rec["salt"])
    expected = bytes.fromhex(rec["hash"])
    got = _pbkdf2(password, salt)
    return hmac.compare_digest(got, expected)

def load_users() -> Dict[str, dict]:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users: Dict[str, dict]) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
