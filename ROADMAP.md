# 🚀 Project Roadmap – Opentrons Secure Protocol Execution

This roadmap defines the next milestones and improvements planned for this project.  
The goal is to make protocol execution on **Opentrons robots** more secure and compliant with quality standards.

---

## ✅ Completed
- [x] Local simulation of protocols with `opentrons.simulate`
- [x] User authentication (username + password) before protocol execution
- [x] User management scripts (`add_user.py`, `remove_user.py`)
- [x] Secure simulation (`secure_simulate.py`)
- [x] Protocol upload and execution on Flex robot via HTTP API (`run_on_flex.py`)
- [x] GitHub repository with documentation (`README.md`, `requirements.txt`)

---

## 📌 Next Steps

### 🔒 Security & Authentication
- [ ] Hash passwords (e.g., bcrypt/argon2) instead of plain text storage
- [ ] Use environment variables for `SECRET_KEY` instead of hardcoding
- [ ] Add user roles (e.g., **admin**, **operator**)

### 🤖 Protocol Execution
- [ ] Add support for OT-2 robot (in addition to Flex)
- [ ] Improve error handling when uploading protocols to the robot
- [ ] Implement automatic logging of executed protocols (who/when/which protocol)

### 📊 Logging & Audit
- [ ] Store logs of all protocol runs with **username, date, success/failure**
- [ ] Export logs as CSV/JSON for compliance
- [ ] Add option to digitally sign logs (integrity check)

### 🖥️ Developer Experience
- [ ] Add unit tests for authentication system
- [ ] Add CI/CD with GitHub Actions (linting + tests)
- [ ] Dockerize the project for easier deployment

### 📦 Future Features
- [ ] Web dashboard for managing users and running protocols
- [ ] Integration with external authentication providers (LDAP, OAuth2)
- [ ] Multi-user sessions with tokens instead of passwords

---

## 🗓️ Timeline
- **Short term (1–2 months):** Password hashing, better error handling, logging system.  
- **Mid term (3–6 months):** Role management, audit exports, CI/CD.  
- **Long term (6–12 months):** Web dashboard, external authentication, enterprise-ready security.  

---
