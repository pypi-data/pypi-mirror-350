import yaml
import os

def load_config(filename=None):
    if filename:
        with open(filename, "r") as f:
            data = yaml.safe_load(f)
        return data
    # otherwise, env
    return {
        "tunnels": os.getenv("TUNNELS", ""),
        "ssh_user": os.getenv("SSH_USER", "root"),
        "ssh_host": os.getenv("SSH_HOST", "localhost"),
        "key_path": os.getenv("KEY_PATH", str(os.path.expanduser("~/.ssh/id_ed25519")))
    }
