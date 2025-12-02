#!/usr/bin/env python3
import os
import sys
import time
import hashlib
import requests
from pathlib import Path

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ENGINE_URLS = [
    # Primary
    "https://raw.githubusercontent.com/laziestlarry/AutonomaX_Commander_Engine/main/engine.zip",

    # Add optional fallback mirrors
    # "https://github.com/.../engine.zip?raw=1",
    # "https://cloudflare-ipfs.com/ipfs/<hash>",
]

ENGINE_ZIP_PATH = Path("engine_download.zip")

# Optional checksum (leave empty to skip)
EXPECTED_SHA256 = ""


# --------------------------------------------------
# UTILS
# --------------------------------------------------

def sha256_file(path: Path) -> str:
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_with_retries(url: str, dest: Path, attempt_limit: int = 3) -> bool:
    """Robust downloader with retries."""
    print(f"[Installer] Trying URL: {url}")

    for attempt in range(1, attempt_limit + 1):
        try:
            print(f"[Installer] Attempt {attempt}/{attempt_limit}...")
            with requests.get(url, stream=True, timeout=20) as r:
                r.raise_for_status()

                total = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                pct = (downloaded / total) * 100
                                print(f"\r[Installer] Downloading: {pct:0.2f}% ", end="")

                print("\n[Installer] Download completed successfully.")
                return True

        except Exception as e:
            print(f"[Installer] Error: {e}")
            if attempt < attempt_limit:
                print("[Installer] Retrying in 2 seconds...")
                time.sleep(2)

    print("[Installer] All attempts failed for this URL.")
    return False


# --------------------------------------------------
# MAIN DOWNLOAD LOGIC
# --------------------------------------------------

def download_engine() -> Path:
    print("[Installer] Starting engine download...")

    # Remove old partial file
    if ENGINE_ZIP_PATH.exists():
        ENGINE_ZIP_PATH.unlink()

    for url in ENGINE_URLS:
        success = download_with_retries(url, ENGINE_ZIP_PATH)
        if success:
            # Optional checksum validation
            if EXPECTED_SHA256:
                digest = sha256_file(ENGINE_ZIP_PATH)
                if digest.lower() != EXPECTED_SHA256.lower():
                    print("[Installer] Checksum mismatch! Download corrupted.")
                    ENGINE_ZIP_PATH.unlink()
                    continue  # try next URL
            return ENGINE_ZIP_PATH

    print("[Installer] ❌ Unable to download engine from any source.")
    sys.exit(1)


# --------------------------------------------------
# MAIN INSTALLER
# --------------------------------------------------

def install():
    print("=== AutonomaX Commander Engine Installer ===")

    zip_path = download_engine()
    print(f"[Installer] Engine ZIP downloaded to: {zip_path}")

    # Unpack
    import zipfile
    print("[Installer] Extracting...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall("engine")

    print("[Installer] Engine extracted to ./engine")
    print("[Installer] Installation complete ✨")


if __name__ == "__main__":
    install()
