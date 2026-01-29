import os
import sys
import subprocess
import ctypes
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION (STRICTEMENT IDENTIQUE AU PROTECTEUR) ---
HARDCODED_KEY = b'u_V8X6-T9pZ2_Wj5Yk_R8f_1vXm_4nE3pL6z8A_B4C0='
cipher = Fernet(HARDCODED_KEY)
EXTENSION = ".locked"
NOTE_NAME = "RECOVERY_INSTRUCTIONS.txt"
NORMAL_WALLPAPER = r"C:\Windows\Web\Wallpaper\Windows\img0.jpg"

user_profile = os.environ.get('USERPROFILE')
TARGET_DIRS = [
    os.path.join(user_profile, 'Desktop'),
    os.path.join(user_profile, 'Documents'),
    os.path.join(user_profile, 'Videos'),
    os.path.join(user_profile, 'AppData', 'Roaming')
]

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def restore_network():
    subprocess.run("ipconfig /renew", shell=True, capture_output=True)

def restore_wallpaper():
    if os.path.exists(NORMAL_WALLPAPER):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, NORMAL_WALLPAPER, 3)

def resurrect_data(file_path):
    # Supprimer les notes
    if file_path.endswith(NOTE_NAME):
        try: os.remove(file_path); return
        except: pass

    # Déchiffrer
    if file_path.endswith(EXTENSION):
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            original_path = file_path.replace(EXTENSION, "")
            with open(original_path, "wb") as f:
                f.write(decrypted_data)
            os.remove(file_path)
        except:
            pass

def main():
    # Force les droits Admin pour le réseau et le registre
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("--- PROTOCOLE DE RESURRECTION EN COURS ---")
    
    restore_network()
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        for target in TARGET_DIRS:
            if not os.path.exists(target): continue
            for root, _, files in os.walk(target):
                for file in files:
                    executor.submit(resurrect_data, os.path.join(root, file))

    restore_wallpaper()
    
    ctypes.windll.user32.MessageBoxW(0, "Systeme restaure avec succes.", "Necro_Resurrection", 0x40)

if __name__ == "__main__":
    main()