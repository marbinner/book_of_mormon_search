import os
import requests
from pathlib import Path

def download_file(url: str, destination: Path):
    """Download a file from URL to destination if it doesn't exist."""
    if destination.exists():
        print(f"✓ {destination.name} already exists")
        return

    print(f"Downloading {destination.name} from GitHub release...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Progress: {percent:.1f}%", end='', flush=True)

    print(f"\n✓ Downloaded {destination.name}")

def ensure_data_files():
    """Download embedding files from GitHub release if they don't exist."""
    data_dir = Path("data")

    # GitHub release URLs
    BASE_URL = "https://github.com/marbinner/book_of_mormon_search/releases/download/v1.0"

    files = [
        (f"{BASE_URL}/bom_embeddings.npz", data_dir / "bom_embeddings.npz"),
        (f"{BASE_URL}/kjb_embeddings.npz", data_dir / "kjb_embeddings.npz"),
        (f"{BASE_URL}/bom_embeddings_normalized.npz", data_dir / "bom_embeddings_normalized.npz"),
        (f"{BASE_URL}/kjb_embeddings_normalized.npz", data_dir / "kjb_embeddings_normalized.npz"),
    ]

    for url, destination in files:
        try:
            download_file(url, destination)
        except Exception as e:
            print(f"Warning: Could not download {destination.name}: {e}")

if __name__ == "__main__":
    ensure_data_files()
