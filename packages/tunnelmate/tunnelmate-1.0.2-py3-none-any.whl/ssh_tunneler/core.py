import os
import subprocess
import time
from pathlib import Path
import re

class SSHTunnel:
    def __init__(self, tunnels, key_path, tunnel_name=None):
        self.remote_host = "srv.us"
        self.tunnels = tunnels  # لیست دیکشنری: [{local_host, local_port}, ...]
        self.key_path = key_path
        self.tunnel_name = tunnel_name or "multi_tunnel"

    def ensure_ssh_key(self):
        key = Path(self.key_path)
        if not key.exists():
            key.parent.mkdir(parents=True, exist_ok=True)
            print(f"🔑 No SSH key found at {self.key_path}. Generating new keypair...")
            subprocess.run([
                "ssh-keygen", "-t", "ed25519", "-N", "", "-f", self.key_path
            ], check=True)
            print("✅ Key created successfully! Below is your public key:")
            pub = open(str(key) + ".pub").read()
            print(f"\n{pub}\n")
            print("👆 Copy this key to your server's ~/.ssh/authorized_keys and rerun the command.")

    def run_tunnel(self, auto_reconnect=True, on_tunnel_link=None):
        self.ensure_ssh_key()
        ssh_cmd = [
            "ssh", "-o", "ExitOnForwardFailure=yes", "-o", "ServerAliveInterval=60",
            "-i", self.key_path,
        ]
        for idx, t in enumerate(self.tunnels):
            ssh_cmd += ["-R", f"{idx+1}:{t['local_host']}:{t['local_port']}"]
        ssh_cmd += [f"{self.remote_host}"]

        desc = " | ".join(
            [f"-R {idx+1}:{t['local_host']}:{t['local_port']}" for idx, t in enumerate(self.tunnels)]
        )
        while True:
            print(f"🚀 Starting tunnel [{self.tunnel_name}] ({self.remote_host} {desc})")
            proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            try:
                for line in proc.stdout:
                    line = line.strip()
                    print(f"[{self.tunnel_name}] {line}")
                    # اگر callback ثبت شده بود و خط لینک تونل را پیدا کردیم
                    if on_tunnel_link is not None:
                        match = re.match(r"^(\d+): (https?://[^\s]+srv\.us/.*)$", line)
                        if match:
                            idx = int(match.group(1)) - 1
                            link = match.group(2)
                            on_tunnel_link(idx, link)
                proc.wait()
            except Exception as e:
                print(f"[{self.tunnel_name}] Error: {e}")
            print(f"[{self.tunnel_name}] Tunnel closed! Retrying in 5s 💫")
            if not auto_reconnect:
                break
            time.sleep(5)
