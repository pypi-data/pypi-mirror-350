# tunnelmate

🚀 **A robust SSH tunnel and automatic Cloudflare DNS management library & CLI**

Easily create, manage, and auto-reconnect SSH tunnels—with automatic SSH key generation and seamless Cloudflare CNAME linking. Use as a Python library or a lightning-fast CLI tool.

---

## Installation

```bash
pip install .
```

---

## CLI Usage

```bash
tunnelmate \
  --tunnel localhost:3000:my-app.example.com \
  --cf-zone-id <ZONE_ID> \
  --cf-api-token <API_TOKEN>
```
The tool will generate an SSH key if not already present and prints the public key to add to your destination server.

---

## Library Usage

```python
from tunnelmate.core import SSHTunnel

tunnels = [
    {"local_host": "localhost", "local_port": 3000, "subdomain": "my-app.example.com"},
]

t = SSHTunnel(
    tunnels=tunnels,
    key_path="/root/.ssh/id_ed25519"
)
t.run_tunnel()
```

---

## Features

- Autogenerates SSH keys if not found, and prints your public key.
- Automatic reconnection if the tunnel closes.
- Accepts all configuration—ports, hosts, Cloudflare API and DNS details—from CLI, environment, or YAML.
- Live logs and easy-to-use interface for managing as many tunnels as you want.
- CLI and Python API both supported.
- Clean, maintainable code—ready to extend or integrate.

---

## Cloudflare CNAME Update Example (Python):

```python
from tunnelmate.cloudflare import update_cname

resp = update_cname(
    zone_id="yourZoneId",
    api_token="yourToken",
    subdomain="my-app.example.com",
    content="target.example.com"
)
print(resp)
```

---

## Folder structure

```
ssh_tunneler/
  core.py         # Tunnel and key handling core logic
  cli.py          # Command-line interface (entrypoint)
  config.py       # Loading config from yaml/env
  cloudflare.py   # Cloudflare DNS API routines
  ssh_utils.py    # SSH key/tool helpers
  __init__.py
setup.py
README.md
```

---

Developed by Parsa Lakzian  
Architected by Tara AI
