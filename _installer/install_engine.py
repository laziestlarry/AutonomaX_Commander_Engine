import os
import zipfile
import urllib.request
from pathlib import Path

ENGINE_ZIP_URL = (
    "https://raw.githubusercontent.com/laziestlarry/AutonomaX_Commander_Engine/main/AutonomaX_Commander_Engine.zip"
)

def download_engine(zip_path="AutonomaX_Commander_Engine.zip"):
    print("[AutonomaX Installer] Downloading engine package...")
    urllib.request.urlretrieve(ENGINE_ZIP_URL, zip_path)
    return zip_path

def extract_engine(zip_path, target="engine"):
    print("[AutonomaX Installer] Extracting engine...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(target)
    print(f"[AutonomaX Installer] Engine installed under: {target}/")
    os.remove(zip_path)

def ensure_structure():
    Path("engine").mkdir(exist_ok=True)
    Path("installer").mkdir(exist_ok=True)

def main():
    print("=== AutonomaX Commander Engine Installer ===")
    ensure_structure()
    zip_path = download_engine()
    extract_engine(zip_path)
    print("Installation complete.")
    print("Your repo is now AutonomaX-Engine compatible.")

if __name__ == "__main__":
    main()
