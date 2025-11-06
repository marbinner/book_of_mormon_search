import os
import requests
from pathlib import Path

def download_file(url: str, destination: Path):
    """Download a file from URL to destination if it doesn't exist."""
    if destination.exists():
        print(f"✓ {destination.name} already exists, skipping download")
        return

    print(f"Downloading {destination.name}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)

    print(f"\n✓ Downloaded {destination.name}")

def ensure_data_files():
    """Download embedding files if they don't exist."""
    data_dir = Path("data")

    # URLs for the embedding files
    # TODO: Replace these with your actual URLs after uploading
    BOM_EMBEDDINGS_URL = os.getenv("BOM_EMBEDDINGS_URL", "")
    KJB_EMBEDDINGS_URL = os.getenv("KJB_EMBEDDINGS_URL", "")

    if not BOM_EMBEDDINGS_URL or not KJB_EMBEDDINGS_URL:
        print("WARNING: Embedding URLs not configured. Set BOM_EMBEDDINGS_URL and KJB_EMBEDDINGS_URL environment variables.")
        return

    # Download files if needed
    download_file(BOM_EMBEDDINGS_URL, data_dir / "bom_embeddings.npz")
    download_file(KJB_EMBEDDINGS_URL, data_dir / "kjb_embeddings.npz")

if __name__ == "__main__":
    ensure_data_files()
