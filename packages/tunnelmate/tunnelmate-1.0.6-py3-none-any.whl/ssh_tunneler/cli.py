import argparse
import logging
from pathlib import Path
from .core import SSHTunnel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def print_tunnel_link(link):
    logging.info(f"Tunnel link: {link}")

def main():
    parser = argparse.ArgumentParser(description='Easy SSH tunnel manager (auto keygen, optional Cloudflare DNS update)')
    # remote_host ثابت و هاردکد شده، remote_port حذف شد
    parser.add_argument("--tunnel", help="Tunnel spec: [host]:port[:subdomain]  (repeatable)", action="append", required=True)
    parser.add_argument("--key-path", help="SSH key location", default=str(Path.home() / ".ssh" / "id_ed25519"))
    parser.add_argument("--name", help="Tunnel name", default=None)
    parser.add_argument("--no-reconnect", action="store_true", help="Do not auto reconnect")
    # Cloudflare (اختیاری)
    parser.add_argument("--cf-zone-id", help="Cloudflare zone_id", default=None)
    parser.add_argument("--cf-record-id", help="Cloudflare record_id", default=None)
    parser.add_argument("--cf-api-token", help="Cloudflare API token", default=None)
    parser.add_argument("--cf-subdomain", help="Cloudflare subdomain (can be used multiple times, one per tunnel)", action="append", default=None)
    parser.add_argument("--cf-content", help="Cloudflare target content (e.g., CNAME)", default=None)
    args = parser.parse_args()

    use_cf = all([
        args.cf_zone_id,
        args.cf_record_id,
        args.cf_api_token
    ])

    # Parse tunnels
    tunnels = []
    for t in args.tunnel:
        # Format: host:port[:subdomain]  یا فقط port
        parts = t.split(":")
        if len(parts) == 3:
            local_host, local_port, subdomain = parts
            local_host = local_host.strip() if local_host.strip() else "localhost"
            local_port = int(local_port.strip())
            subdomain = subdomain.strip()
        elif len(parts) == 2:
            local_host, local_port = parts
            local_host = local_host.strip() if local_host.strip() else "localhost"
            local_port = int(local_port.strip())
            subdomain = None
        else:
            local_host = "localhost"
            local_port = int(parts[0].strip())
            subdomain = None
        tunnels.append({"local_host": local_host, "local_port": local_port, "subdomain": subdomain})

    tun = SSHTunnel(
        tunnels=tunnels,
        key_path=args.key_path,
        tunnel_name=args.name
    )

    if use_cf:
        from .cloudflare import update_cname
        logging.info("Updating Cloudflare DNS record ...")
    else:
        logging.info("No Cloudflare info provided. Only SSH tunnel will be established.")

    def on_tunnel_link(idx, link):
        import re
        tun_item = tunnels[idx]
        subdomain = tun_item["subdomain"]
        print_tunnel_link(link)
        if subdomain and use_cf:
            # only domain (no http) as content
            domain = re.sub(r"^https?://([^/]+)/?.*$", r"\1", link)
            from .cloudflare import update_cname
            logging.info(f"Updating Cloudflare DNS: {subdomain} → {domain} (CDN Proxy: OFF) ...")
            cf_result = update_cname(
                zone_id=args.cf_zone_id,
                api_token=args.cf_api_token,
                subdomain=subdomain,
                content=domain,
                proxied=False,
                record_id=args.cf_record_id if args.cf_record_id else None
            )
            logging.info(f"CNAME {subdomain} → {domain} (Proxy disabled):")
            logging.info(cf_result)

    tun.run_tunnel(auto_reconnect=not args.no_reconnect, on_tunnel_link=on_tunnel_link)

if __name__ == "__main__":
    main()
