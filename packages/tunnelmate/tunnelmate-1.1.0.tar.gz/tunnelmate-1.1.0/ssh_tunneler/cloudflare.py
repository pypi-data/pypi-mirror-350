import requests

def update_cname(zone_id, api_token, subdomain, content, proxied=True, record_id=None):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "type": "CNAME",
        "name": subdomain,
        "content": content,
        "ttl": 120,
        "proxied": proxied,
    }
    
    # Try to create; if already exists (81053), then PATCH by name.
    r = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        headers=headers,
        json=data
    )
    result = r.json()
    # 81053 = An A, AAAA, or CNAME record with that host already exists.
    if (not result.get("success")) and result.get("errors") and any((str(e.get("code")) == "81053") for e in result.get("errors")):
        for attempt in range(3):
            # Find record_id for subdomain
            rr = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={subdomain}",
                headers=headers,
            )
            info = rr.json()
            deleted = False
            if info.get("result"):
                for rec in info["result"]:
                    if rec["name"] == subdomain:
                        rid = rec["id"]
                        rdel = requests.delete(
                            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{rid}",
                            headers=headers
                        )
                        deleted = True
            if deleted:
                import time
                time.sleep(2)
                # Now create CNAME
                rpost = requests.post(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                    headers=headers,
                    json=data
                )
                r = rpost.json()
                if r.get("success"):
                    return r
            else:
                break  # No matching record found, stop retry loop
        return r  # Return the last attempt's result
    return result
