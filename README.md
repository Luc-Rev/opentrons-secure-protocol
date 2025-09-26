# Opentrons Secure Protocol Execution

This project provides a secure way to run and simulate **Opentrons protocols** (OT-2 and Flex) with **user authentication**.  
It adds a simple user/password system before a protocol can be executed, ensuring compliance with quality standards.

---

## 🚀 Features
- User authentication (username + password) before running a protocol.
- Protocol simulation locally (with `opentrons.simulate`).
- Protocol execution directly on an Opentrons **Flex** robot via its HTTP API.
- User management (add, remove, list users).
- Example secure protocol included (`mon_protocole.py`).

---

## 📂 Project Structure

Opentrons-lucR/
├── mon_protocole.py # Example secure protocol (requires authentication)
├── simulate_run.py # Run a protocol in simulation mode
├── secure_simulate.py # Same, but requires user login
├── run_on_flex.py # Upload and run a protocol on the Flex robot
├── auth_utils.py # Utilities to manage users (add/remove/list)
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/opentrons-secure-protocol.git
   cd opentrons-secure-protocol

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows (PowerShell)

3. Install dependencies:

pip install -r requirements.txt

🧪 Usage

1. Manage users

python auth_utils.py definition 
python add_user.py add <username> <password>
python remove_user.py remove <username>

2. Create your protocole 

Edit your protocole and creat your SECRET_KEY and TOKEN_FILENAME

python mon_protocole.py

3. Run a simulation (with authentication)

python secure_simulate.py 

You will be prompted for a username and password before the simulation starts.

4. Run on an Opentrons Flex 

Edit run_on_flex.py to set your robot’s IP address

python run_on_flex.py


📌 Notes

Requires Python 3.10+.

Works with Opentrons Flex.

Authentication is file-based (simple JSON). For production, integrate with a secure system (e.g., database, hashed passwords, signed tokens).