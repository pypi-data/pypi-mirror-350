"""Main file for the client."""

import json
import os
import requests
import sys

CLIENT_KB_DIR = os.path.join(os.getcwd(), ".luca")
LOCAL_KB_PATH = os.path.join(CLIENT_KB_DIR, "kb.txt")
CLIENT_ARTIFACTS_DIR = os.path.join(CLIENT_KB_DIR, "artifacts")

SERVER_URL = "http://45.33.41.244:8000"

def ensure_dirs():
    """Ensure the client's directories exist."""
    for directory in [CLIENT_KB_DIR, CLIENT_ARTIFACTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def ensure_kb_dir():
    """Ensure the client's KB directory exists."""
    if not os.path.exists(CLIENT_KB_DIR):
        os.makedirs(CLIENT_KB_DIR)


def sync_kb():
    """Sync the knowledge base from the server."""
    ensure_kb_dir()
    response = requests.get(f"{SERVER_URL}/kb")
    response.raise_for_status()
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(json.loads(response.content)["text"])


def update_kb(content: str):
    """Update the knowledge base."""
    ensure_kb_dir()
    kb_text = json.loads(content)["text"]
    with open(LOCAL_KB_PATH, "w") as f:
        f.write(kb_text)

def download_artifact(filename: str) -> bool:
    """Download a specific artifact from the server."""
    try:
        response = requests.get(f"{SERVER_URL}/artifacts/{filename}")
        response.raise_for_status()
        
        local_path = os.path.join(CLIENT_ARTIFACTS_DIR, filename)
        with open(local_path, "wb") as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading artifact {filename}: {e}")
        return False


def download_artifacts(artifacts: list) -> list:
    """Download multiple artifacts and return successful downloads."""
    ensure_dirs()
    downloaded = []
    
    for artifact in artifacts:
        filename = artifact["filename"]
        size = artifact["size"]
        
        print(f"Downloading {filename} ({size} bytes)...")
        if download_artifact(filename):
            downloaded.append(filename)
            local_path = os.path.join(CLIENT_ARTIFACTS_DIR, filename)
            print(f"✓ Saved to {local_path}")
        else:
            print(f"✗ Failed to download {filename}")
    
    return downloaded

def init():
    """Initialize the client and the server."""
    print("Initializing the client...")
    request_params = {
        "WANDB_API_KEY": os.getenv("WANDB_API_KEY"),
        "WANDB_ENTITY": os.getenv("WANDB_ENTITY")
    }
    try:
        response = requests.post(f"{SERVER_URL}/init", json=request_params)
        response.raise_for_status()
        update_kb(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error initializing server: {e}")

def feedback(text: str):
    """Send feedback to the server."""
    response = requests.post(f"{SERVER_URL}/feedback", json={"text": text})
    response.raise_for_status()
    print(json.loads(response.content)["text"])

def list_artifacts():
    """List all available artifacts on the server."""
    try:
        response = requests.get(f"{SERVER_URL}/artifacts")
        response.raise_for_status()
        
        response_data = json.loads(response.content)
        artifacts = response_data.get("artifacts", [])
        
        if not artifacts:
            print("No artifacts available.")
            return
        
        print("Available artifacts:")
        for artifact in artifacts:
            filename = artifact["filename"]
            size = artifact["size"]
            print(f"  {filename} ({size} bytes)")
            
    except requests.exceptions.RequestException as e:
        print(f"Error listing artifacts: {e}")

def main(argv):
    """Main function."""
    if len(argv) == 1:
        print("Usage: luca <command> or luca <prompt>")
        print("Commands:")
        print("  init: Initialize the client and the server.")
        print("  sync: Sync the knowledge base from the server.")
        print("  artifacts: List all available artifacts.\n")
        print("Examples:")
        print("  luca init")
        print("  luca sync")
        print("  luca artifacts")
        print("  luca 'Research papers on reinforcement learning.'")
        return
    if argv[1] == "init":
        init()
    elif argv[1] == "sync":
        sync_kb()
        print("Knowledge base synced successfully!")
    elif argv[1] == "artifacts":
        list_artifacts()
    elif argv[1] == "feedback":
        feedback(argv[2])
    else:
        # User query
        prompt = argv[1]
        response = requests.post(f"{SERVER_URL}/query", json={"prompt": prompt})
        response.raise_for_status()
        
        response_data = json.loads(response.content)
        print(response_data["text"])
        
        # Handle artifacts
        artifacts = response_data.get("artifacts", [])
        if artifacts:
            print(f"\n[Found {len(artifacts)} new artifact(s)]")
            downloaded = download_artifacts(artifacts)
            if downloaded:
                print(f"[Downloaded {len(downloaded)} artifact(s) successfully]")
        
        # Check if KB was updated and sync if needed
        if response_data.get("kb_updated", False):
            print("\n[Syncing knowledge base...]")
            sync_kb()
            print("[Knowledge base synced successfully!]")


def entrypoint():
    """Entry point for the CLI tool."""
    main(sys.argv)


if __name__ == "__main__":
    entrypoint()
