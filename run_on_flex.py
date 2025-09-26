# run_on_flex.py
import os, time, hmac, hashlib, secrets, json, requests
from getpass import getpass
from datetime import datetime
from auth_utils import load_users, verify_user

# ==== CONFIG ====
ROBOT = os.environ.get("ROBOT", "http://XXX.XXX.XX.XXX:31950")  # set ROBOT env var or edit here
PROTOCOL_PATH = "mon_protocole.py"
TOKEN_FILENAME = "auth_token.txt"
AUDIT_LOG = "audit.log"

# Must MATCH the secret in mon_protocole.py
SECRET_KEY = b""
TOKEN_TTL_SECONDS = 600

HEADERS = {
    "Opentrons-Version": "3",  # << REQUIRED by Flex HTTP API
}

def make_token(username: str) -> str:
    ts = int(time.time())
    nonce = secrets.token_hex(8)
    msg = f"{username}|{ts}|{nonce}".encode("utf-8")
    sig = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
    return f"{username}|{ts}|{nonce}|{sig}"

def audit(line: str):
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {line}\n")

def pretty_status(state: dict) -> str:
    try:
        return state["data"]["status"]
    except Exception:
        return "unknown"

if __name__ == "__main__":
    # 0) Local login
    user = input("User: ").strip()
    pwd = getpass("Password: ")
    users = load_users()
    if not verify_user(users, user, pwd):
        raise SystemExit("⛔ Auth failed")

    # (optional) quick health check
    try:
        h = requests.get(f"{ROBOT}/health", headers=HEADERS, timeout=5)
        print("Health:", h.status_code, h.text[:120], "...")
    except Exception as e:
        print("⚠️  Could not reach robot /health:", e)

    # 1) Generate signed token
    token = make_token(user)
    with open(TOKEN_FILENAME, "w", encoding="utf-8") as f:
        f.write(token)

    # 2) Upload protocol + token (multipart; explicit filenames + MIME)
    files = [
        ("files", ("mon_protocole.py", open(PROTOCOL_PATH, "rb"), "text/x-python")),
        ("files", ("auth_token.txt", open(TOKEN_FILENAME, "rb"), "text/plain")),
    ]
    r = requests.post(f"{ROBOT}/protocols", files=files, headers=HEADERS, timeout=30)
    print("UPLOAD STATUS:", r.status_code, r.text)
    r.raise_for_status()
    protocol_id = r.json()["data"]["id"]
    print(f"✅ Uploaded protocol: {protocol_id}")

    # 3) Create run
    payload = {"data": {"protocolId": protocol_id, "labwareOffsets": []}}
    r = requests.post(f"{ROBOT}/runs", json=payload, headers=HEADERS, timeout=30)
    print("CREATE RUN:", r.status_code, r.text)
    r.raise_for_status()
    run_id = r.json()["data"]["id"]
    print(f"✅ Created run: {run_id}")

    # 4) Play run
    r = requests.post(
        f"{ROBOT}/runs/{run_id}/actions",
        json={"data": {"actionType": "play"}},
        headers=HEADERS,
        timeout=30,
    )
    print("PLAY:", r.status_code, r.text)
    r.raise_for_status()
    print("▶️  Run started")

    audit(f"START user={user} protocol={PROTOCOL_PATH} run_id={run_id}")

    # 5) Poll status until terminal
    terminal = {"succeeded", "failed", "stopped", "finished"}
    while True:
        time.sleep(2)
        s = requests.get(f"{ROBOT}/runs/{run_id}", headers=HEADERS, timeout=30)
        s.raise_for_status()
        st = pretty_status(s.json())
        print("status:", st)
        if st in terminal:
            break

    print(f"🏁 Run ended with status: {st}")
    audit(f"END   user={user} run_id={run_id} status={st}")

    # 6) Save command log (optional)
    try:
        log = requests.get(f"{ROBOT}/runs/{run_id}/commands", headers=HEADERS, timeout=30).json()
        with open(f"run_{run_id}.json", "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2)
        print(f"📝 Saved command log to run_{run_id}.json")
    except Exception as e:
        print("Could not fetch command log:", e)