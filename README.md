# Opentrons Secure Protocol Execution & GUI Launcher

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Opentrons](https://img.shields.io/badge/Opentrons-Flex%20%7C%20OT--2-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

Ce projet fournit un environnement sécurisé et une **interface graphique (GUI)** pour déployer et exécuter des protocoles Python sur un robot **Opentrons Flex**. Il garantit la traçabilité des opérateurs et protège le robot contre les exécutions non autorisées via un système de jetons cryptographiques (HMAC), tout en respectant les standards de qualité des laboratoires.

## ✨ Nouvelles Fonctionnalités (Pro Launcher)
- 🖥️ **Interface Graphique Intégrée :** Plus besoin de terminal. Gérez les opérateurs, sélectionnez vos protocoles et configurez l'IP du robot en quelques clics.
- 🔒 **Authentification Forte (HMAC) :** Le protocole embarque une vérification cryptographique bloquant l'exécution si le jeton n'est pas signé par le lanceur officiel.
- 👤 **Traçabilité & Audit :** Génération automatique d'un `audit.log` et intégration du nom de l'opérateur directement dans l'historique JSON du run sur le Flex.
- 👁️ **Console de Monitoring en Direct :** Suivez les statuts du robot (ex: `blocked-by-open-door`, `running`) directement depuis l'interface visuelle.
- ⚙️ **Gestion des Utilisateurs :** Mots de passe hachés (`pbkdf2_hmac`) et salés localement.

## 🛠️ Installation

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/Luc-Rev/opentrons-secure-protocol.git](https://github.com/Luc-Rev/opentrons-secure-protocol.git)
   cd opentrons-secure-protocol
