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
        # فقط create
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            headers=headers,
            json=data
        )
        return r.json()
