💀 Necro_Ranso Suite : Defensive Cyber-Shield
Necro_Ranso est une solution de cybersécurité offensive-défensive de type "Terre Brûlée". Ce programme est conçu pour être activé instantanément lorsqu'une intrusion humaine ou un malware exfiltrant est détecté sur un serveur sensible.

Au lieu de simplement bloquer l'accès, il neutralise les données en les rendant illisibles pour l'attaquant, tout en isolant la machine du reste du réseau.

🏗️ Architecture de la Suite
La suite repose sur deux piliers principaux agissant en miroir :

1. Necro_Ranso.exe (L'Agent Verrouilleur)
C'est le script de panique. Une fois exécuté, il suit un protocole strict en moins de quelques secondes :

Élévation de Privilèges : Utilise l'API Windows pour forcer un prompt UAC et obtenir les droits NT AUTHORITY\SYSTEM.

Furtivité Totale : Détachement du processus de la console pour une exécution invisible en arrière-plan.

Neutralisation de l'Exfiltration : Exécute ipconfig /release pour couper immédiatement toute communication réseau.

Libération des Handles : Identifie et tue les processus (SQL, Office, Browsers) qui verrouillent les fichiers sensibles pour garantir un chiffrement à 100%.

Chiffrement Symétrique AES-256 : Utilise la bibliothèque cryptography.fernet avec un moteur multi-threadé (35 workers) pour verrouiller les fichiers utilisateur en .locked.

Destruction des Backups : Purge les clichés instantanés de volume (VSS) pour empêcher une restauration via Windows.

Alerte Visuelle : Remplace le fond d'écran système par une image d'alerte (alerte.jpg) intégrée dans les ressources du binaire.

Suicide du Processus : Suppression automatique du fichier exécutable après la fin des opérations pour empêcher l'analyse immédiate de la clé.

2. Necro_ReverseRanso.exe (L'Agent de Résurrection)
Le remède unique. Ce script est destiné à être conservé hors-ligne (clé USB de secours) pour rétablir l'ordre :

Réactivation Réseau : Relance les interfaces via ipconfig /renew pour sortir le serveur de son isolation.

Déchiffrement Récursif : Parcourt les répertoires pour inverser le chiffrement AES et restaurer les extensions originales.

Nettoyage Forensique : Supprime les notes de rançon défensives (RECOVERY_INSTRUCTIONS.txt) et les artefacts de protection.

Résurrection Visuelle : Restaure le fond d'écran d'origine de Windows pour signaler la fin de l'état d'urgence.

📂 Structure du Projet
Plaintext
├── necro_ranso.py           # Code source du verrouilleur
├── necro_reverseranso.py    # Code source du restaurateur (Recovery)
├── alerte.jpg               # Image d'alerte (à inclure dans le binaire)
├── requirements.txt         # Dépendances (cryptography)
└── build/                   # Dossier des exécutables compilés (.exe)
🚀 Guide de Compilation (Deployment)
Pour une efficacité maximale, les scripts doivent être compilés avec Auto-py-to-exe ou PyInstaller.

Paramètres de build recommandés :
One File : Packagé en un seul binaire.

Window Based : Pas de fenêtre CMD pour la discrétion (surtout pour l'agent de verrouillage).

Additional Files : Ajouter alerte.jpg avec le chemin de destination ..

Advanced : Cocher --uac-admin (Indispensable pour le réseau et les fichiers système).

Bash
# Commande pour Necro_Ranso
pyinstaller --onefile --noconsole --uac-admin --add-data "alerte.jpg;." necro_ranso.py

# Commande pour Necro_ReverseRanso
pyinstaller --onefile --console --uac-admin necro_reverseranso.py
🔑 Configuration de la Clé de Sécurité
La sécurité repose sur la clé Fernet stockée dans la variable HARDCODED_KEY.

Attention : En cas de perte de cette clé, les données sont mathématiquement irrécupérables. Elle doit être la même dans les deux scripts.

Python
# Générer une nouvelle clé pour votre déploiement :
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
🛡️ Cas d'Usage
Protection de serveurs sensibles : Verrouillage en cas d'intrusion réseau confirmée.

Défense Anti-Forensics : Rendre les données inutilisables si le matériel est saisi ou volé.

Isolation d'urgence : Coupure réseau et chiffrement en un seul clic.

📜 Licence & Disclaimer
Ce projet est publié sous licence MIT. L'usage de cet outil est sous votre entière responsabilité. Necro_Ranso est un outil de "terre brûlée" ; testez-le toujours dans une machine virtuelle (VM) avant tout déploiement en production.
