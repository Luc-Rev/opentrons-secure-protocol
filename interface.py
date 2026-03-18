import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import json
from datetime import datetime
import threading 
import sys

try:
    from auth_utils import load_users, save_users, create_user
except ImportError:
    messagebox.showerror("Erreur", "Le fichier auth_utils.py est introuvable.")

AUDIT_LOG = "audit.log"

def log_audit(action, target_user, actor="admin_gui"):
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {actor} | {action} | {target_user}\n")

# --- FONCTIONS UTILISATEURS (Identiques) ---
def rafraichir_liste_users():
    combo_users['values'] = list(load_users().keys())
    if combo_users['values']:
        combo_users.current(0)

def ajouter_user():
    def valider_ajout():
        nom = entry_nom.get().strip()
        pwd1 = entry_pwd1.get()
        pwd2 = entry_pwd2.get()
        if not nom or pwd1 != pwd2:
            messagebox.showwarning("Erreur", "Données invalides ou mots de passe différents.")
            return
        users = load_users()
        if nom in users:
            messagebox.showwarning("Erreur", "Cet utilisateur existe déjà.")
            return
        users = create_user(users, nom, pwd1)
        save_users(users)
        log_audit("ADD_USER", nom)
        messagebox.showinfo("Succès", f"Utilisateur '{nom}' ajouté.")
        rafraichir_liste_users()
        fenetre_ajout.destroy()

    fenetre_ajout = tk.Toplevel(app)
    fenetre_ajout.title("Ajouter utilisateur")
    fenetre_ajout.geometry("300x250")
    tk.Label(fenetre_ajout, text="Nom :").pack(pady=5)
    entry_nom = tk.Entry(fenetre_ajout)
    entry_nom.pack()
    tk.Label(fenetre_ajout, text="Mot de passe :").pack(pady=5)
    entry_pwd1 = tk.Entry(fenetre_ajout, show="*")
    entry_pwd1.pack()
    tk.Label(fenetre_ajout, text="Confirmer :").pack(pady=5)
    entry_pwd2 = tk.Entry(fenetre_ajout, show="*")
    entry_pwd2.pack()
    tk.Button(fenetre_ajout, text="Ajouter", command=valider_ajout, bg="#4CAF50", fg="white").pack(pady=15)

def supprimer_user():
    nom = combo_users.get()
    if nom and messagebox.askyesno("Confirmation", f"Supprimer {nom} ?"):
        users = load_users()
        del users[nom]
        save_users(users)
        log_audit("REMOVE_USER", nom)
        rafraichir_liste_users()

def choisir_protocole():
    chemin = filedialog.askopenfilename(filetypes=[("Fichiers Python", "*.py")])
    if chemin:
        label_chemin_proto.config(text=chemin)

# --- NOUVEAUTÉ : LOGIQUE D'EXÉCUTION SANS TERMINAL ---

def executer_en_arriere_plan(env):
    """Cette fonction tourne dans un thread séparé pour lire les logs du robot en direct."""
    try:
        dossier_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin_script = os.path.join(dossier_actuel, "run_on_flex.py")
        
        # --- NOUVEAU 1 : On force Python à utiliser l'UTF-8 dans son environnement ---
        env["PYTHONIOENCODING"] = "utf-8"
        
        process = subprocess.Popen(
            [sys.executable, chemin_script],
            env=env,
            cwd=dossier_actuel,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8", # <--- NOUVEAU 2 : On lit la sortie en UTF-8
            creationflags=subprocess.CREATE_NO_WINDOW 
        )
        
        for ligne in iter(process.stdout.readline, ''):
            if not ligne:
                break
            app.after(0, ecrire_console, ligne)
            
        process.stdout.close()
        process.wait()
        app.after(0, ecrire_console, "\n🏁 Processus terminé.\n")
        
    except Exception as e:
        app.after(0, ecrire_console, f"\n❌ Erreur système : {e}\n")
    
    app.after(0, lambda: btn_run.config(state=tk.NORMAL))

def ecrire_console(texte):
    """Ajoute du texte dans la zone noire en bas de l'interface"""
    zone_console.insert(tk.END, texte)
    zone_console.see(tk.END) # Fait défiler automatiquement vers le bas

def lancer_run():
    robot_ip = entree_ip.get().strip()
    protocole_path = label_chemin_proto.cget("text")
    user = combo_users.get()
    pwd = entree_pwd_run.get() # On récupère le mot de passe tapé dans l'interface
    
    if protocole_path == "Aucun fichier sélectionné":
        messagebox.showerror("Erreur", "Veuillez sélectionner un protocole.")
        return
    if not pwd:
        messagebox.showerror("Erreur", "Veuillez taper votre mot de passe pour lancer le run.")
        return

    # Préparation des variables cachées
    env = os.environ.copy()
    env["ROBOT"] = robot_ip
    env["PROTOCOL_PATH"] = protocole_path
    env["OT_USER"] = user
    env["OT_PWD"] = pwd

    # On nettoie la console et on désactive le bouton pour éviter les doubles clics
    zone_console.delete(1.0, tk.END)
    btn_run.config(state=tk.DISABLED)
    ecrire_console(f"🚀 Lancement initié par {user}...\n")
    
    # Lancement du script dans le thread en arrière-plan
    threading.Thread(target=executer_en_arriere_plan, args=(env,), daemon=True).start()

# --- CRÉATION DE LA FENÊTRE PRINCIPALE ---
app = tk.Tk()
app.title("Flex Secure Launcher Pro")
app.geometry("550x700") # Fenêtre un peu plus grande
app.configure(padx=20, pady=20)

# Section Utilisateurs
frame_users = tk.Frame(app)
frame_users.pack(fill="x", pady=5)
combo_users = ttk.Combobox(frame_users, state="readonly", width=25)
combo_users.pack(side="left", padx=(0, 10))
rafraichir_liste_users()
tk.Button(frame_users, text="➕ Ajouter", command=ajouter_user).pack(side="left", padx=5)
tk.Button(frame_users, text="❌ Supprimer", command=supprimer_user).pack(side="left", padx=5)

# Section Authentification d'Exécution
frame_auth = tk.Frame(app)
frame_auth.pack(fill="x", pady=5)
tk.Label(frame_auth, text="Mot de passe pour lancer :", fg="red").pack(side="left")
entree_pwd_run = tk.Entry(frame_auth, show="*", width=20)
entree_pwd_run.pack(side="left", padx=10)

tk.Frame(app, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

# Section Robot & Protocole
tk.Label(app, text="Configuration Robot (IP) :").pack(anchor="w")
entree_ip = tk.Entry(app, width=50)
entree_ip.insert(0, "http://192.168.15.185:31950")
entree_ip.pack(anchor="w", pady=(0, 10))

tk.Button(app, text="📂 Choisir le fichier .py", command=choisir_protocole).pack(anchor="w")
label_chemin_proto = tk.Label(app, text="Aucun fichier sélectionné", fg="blue", wraplength=500, justify="left")
label_chemin_proto.pack(anchor="w", pady=(5, 15))

# Bouton de lancement
btn_run = tk.Button(app, text="🚀 LANCER LE PROTOCOLE", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=lancer_run)
btn_run.pack(fill="x", pady=5)

# --- NOUVEAUTÉ : LA CONSOLE INTÉGRÉE ---
tk.Label(app, text="Logs du Robot en direct :").pack(anchor="w", pady=(10, 0))
zone_console = tk.Text(app, height=12, bg="black", fg="#00FF00", font=("Consolas", 9))
zone_console.pack(fill="both", expand=True)

app.mainloop()