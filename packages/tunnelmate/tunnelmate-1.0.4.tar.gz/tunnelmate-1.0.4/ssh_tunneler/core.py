import os
import subprocess
import time
import logging
from pathlib import Path
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class SSHTunnel:
    def __init__(self, tunnels, key_path, tunnel_name=None):
        self.remote_host = "srv.us"
        self.tunnels = tunnels  # list of dict: [{local_host, local_port}, ...]
        self.key_path = key_path
        self.tunnel_name = tunnel_name or "multi_tunnel"

    def ensure_ssh_key(self):
        key = Path(self.key_path)
        if not key.exists():
            key.parent.mkdir(parents=True, exist_ok=True)
            logging.info(f"No SSH key found at {self.key_path}. Generating new ed25519 keypair…")
            subprocess.run([
                "ssh-keygen", "-t", "ed25519", "-N", "", "-f", self.key_path
            ], check=True)
            logging.info("SSH key created successfully! Public key is below:")
            pub = open(str(key) + ".pub").read()
            print(f"\n{pub}\n")
            logging.warning("Copy this public key to your remote server's ~/.ssh/authorized_keys and rerun the command.")

    def run_tunnel(self, auto_reconnect=True, on_tunnel_link=None):
        self.ensure_ssh_key()
        ssh_cmd = [
            "ssh",
            "-T",
            "-o", "ExitOnForwardFailure=yes",
            "-o", "ServerAliveInterval=60",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-i", self.key_path,
        ]
        for idx, t in enumerate(self.tunnels):
            ssh_cmd += ["-R", f"{idx+1}:{t['local_host']}:{t['local_port']}"]
        ssh_cmd += [f"{self.remote_host}"]

        desc = " | ".join(
            [f"-R {idx+1}:{t['local_host']}:{t['local_port']}" for idx, t in enumerate(self.tunnels)]
        )
        while True:
            logging.info(f"Starting tunnel [{self.tunnel_name}] {self.remote_host} {desc}")
            proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            try:
                for line in proc.stdout:
                    line = line.strip()
                    logging.info(f"[{self.tunnel_name}] {line}")
                    if on_tunnel_link is not None:
                        match = re.match(r"^(\d+): (https?://[^\s]+srv\.us/.*)$", line)
                        if match:
                            idx = int(match.group(1)) - 1
                            link = match.group(2)
                            on_tunnel_link(idx, link)
                proc.wait()
            except Exception as e:
                logging.error(f"[{self.tunnel_name}] Error: {e}")
            logging.warning(f"[{self.tunnel_name}] Tunnel closed! Retrying in 5 seconds.")
            if not auto_reconnect:
                break
            time.sleep(5)
