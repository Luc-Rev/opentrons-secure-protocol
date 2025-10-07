# Opentrons Secure Protocol Execution

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Opentrons](https://img.shields.io/badge/Opentrons-Flex%20%7C%20OT--2-green)

This project provides a secure way to run and simulate **Opentrons protocols** (OT-2 and Flex) with **user authentication**.  
It adds a simple user/password system before a protocol can be executed, ensuring compliance with quality standards.

---

## 🚀 Features
- 🔑 User authentication (username + password) before running a protocol.  
- 🧪 Protocol simulation locally (with `opentrons.simulate`).  
- 🤖 Protocol execution directly on an Opentrons **Flex** robot via its HTTP API.  
- 👤 User management (add, remove, list users).  
- 📄 Example secure protocol included (`mon_protocole.py`).  

---

## 📂 Project Structure

Opentrons-lucR/
 -- mon_protocole.py # Example secure protocol (requires authentication)
 -- secure_simulate.py # Simulation with authentication
 -- run_on_flex.py # Upload and run a protocol on the Flex robot
 -- auth_utils.py # Utilities to manage users (add/remove/list)
 -- add_user.py # Add new user
 -- remove_user.py # Remove existing user
 -- requirements.txt # Python dependencies
 -- README.md # Project documentation

---

## ⚙️ Installation


Install dependencies:

 
pip install -r requirements.txt
🧪 Usage
1. Manage users
 
python add_user.py <username> <password>
python remove_user.py <username>

2. Create your protocol
Edit mon_protocole.py and configure your:

SECRET_KEY

TOKEN_FILENAME

Run it locally:
 
python mon_protocole.py

3. Run a simulation (with authentication)
 
python secure_simulate.py
You will be prompted for a username and password before the simulation starts.

4. Run on an Opentrons Flex

MATCH the secret code in mon_protocole.py 
Edit run_on_flex.py to set your robot’s IP address, then run:

python run_on_flex.py
📌 Notes
Requires Python 3.10+.

Works with Opentrons Flex (and simulation mode for OT-2).
Authentication is file-based (JSON) → simple demo purpose.



