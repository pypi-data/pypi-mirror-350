import subprocess
from pathlib import Path

def ensure_ssh_key(key_path):
    key = Path(key_path)
    if not key.exists():
        key.parent.mkdir(parents=True, exist_ok=True)
        print(f"🔑 No SSH key found at {key_path}. Generating a new keypair...")
        subprocess.run([
            "ssh-keygen", "-t", "ed25519", "-N", "", "-f", str(key_path)
        ], check=True)
        print("✅ Key created successfully! Below is your public key:")
        pub = open(str(key) + ".pub").read()
        print(f"\n{pub}\n")
        print("👆 Add this key to your remote server's authorized_keys (or use ssh-copy-id).")
