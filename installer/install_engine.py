import os
import zipfile
import urllib.request
from pathlib import Path

ENGINE_REPO_ZIP = (
    "https://github.com/laziestlarry/AutonomaX_Commander_Engine/archive/refs/heads/main.zip"
)

def download_engine(zip_path: str = "AutonomaX_Commander_Engine_main.zip") -> str:
    print("[AutonomaX Installer] Downloading engine archive...")
    urllib.request.urlretrieve(ENGINE_REPO_ZIP, zip_path)
    return zip_path

def extract_engine(zip_path: str, target: str = "engine"):
    print("[AutonomaX Installer] Extracting engine from archive...")
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    prefix = "AutonomaX_Commander_Engine-main/engine/"

    with zipfile.ZipFile(zip_path, "r") as z:
        members = [m for m in z.namelist() if m.startswith(prefix)]
        if not members:
            raise RuntimeError("No engine/ folder found in archive. Did you commit it?")

        for member in members:
            rel = member[len(prefix):]
            if not rel:
                continue  # skip the folder itself
            dest = target_path / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with z.open(member) as src, open(dest, "wb") as dst:
                dst.write(src.read())

    print(f"[AutonomaX Installer] Engine installed under: {target_path.resolve()}")
    os.remove(zip_path)

def main():
    print("=== AutonomaX Commander Engine Installer ===")
    zip_path = download_engine()
    extract_engine(zip_path)
    print("[AutonomaX Installer] Installation complete.")
    print("Your repo is now AutonomaX-Engine compatible.")

if __name__ == "__main__":
    main()
