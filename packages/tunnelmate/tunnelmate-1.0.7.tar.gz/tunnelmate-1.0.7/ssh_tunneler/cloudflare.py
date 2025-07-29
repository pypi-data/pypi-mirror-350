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
    if record_id:
        # اول PATCH
        r = requests.patch(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,
            json=data
        )
        result = r.json()
        if (not result.get("success")) and result.get("errors") and any((str(e.get("code")) == "81044") for e in result.get("errors")):
            # رکورد وجود ندارد باید بسازیم
            r = requests.post(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                headers=headers,
                json=data
            )
            return r.json()
        return result
    else:
        # Try to create; if already exists (81053), then PATCH by name.
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers=headers,
            json=data
        )
        result = r.json()
        # 81053 = An A, AAAA, or CNAME record with that host already exists.
        if (not result.get("success")) and result.get("errors") and any((str(e.get("code")) == "81053") for e in result.get("errors")):
            # Find record_id for subdomain
            rr = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={subdomain}",
                headers=headers,
            )
            info = rr.json()
            found_id = None
            if info.get("result"):
                for rec in info["result"]:
                    if rec["type"] == "CNAME" and rec["name"] == subdomain:
                        found_id = rec["id"]
                        break
            if found_id:
                # Delete before create
                rq = requests.delete(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{found_id}",
                    headers=headers
                )
                # Now create again
                rpost = requests.post(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                    headers=headers,
                    json=data
                )
                return rpost.json()
        return result
