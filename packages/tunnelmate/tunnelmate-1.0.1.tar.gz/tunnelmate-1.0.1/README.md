# tunnelmate

🚀 **پکیج جامع مدیریت تونل SSH + بروزرسانی خودکار Cloudflare (کتابخانه + CLI)**

یک راهکار آسان و حرفه‌ای برای ایجاد، مدیریت و ریکانکت تونل‌های SSH همراه با ساخت اتوماتیک کلید، دریافت تنظیمات از فایل YAML/ENV/CLI و کار با API کلودفلر.

---

## نصب

```bash
pip install .
```

---

## استفاده به صورت ابزار خط فرمان (CLI)

```bash
tunnelmate \
  --remote-host example.com \
  --remote-port 2222 \
  --local-host localhost \
  --local-port 3000 \
  --remote-user root
```
اگر کلید SSH وجود نداشت خودش می‌سازد و public key را می‌دهد که روی سرور قرار بدهید!

---

## استفاده به عنوان کتابخانه پایتون

```python
from tunnelmate.core import SSHTunnel

tunnel = SSHTunnel(
    remote_host="example.com",
    remote_user="root",
    remote_port=2222,
    local_host="localhost",
    local_port=3000,
    key_path="/root/.ssh/id_ed25519"
)
tunnel.run_tunnel()
```

---

## ویژگی‌ها

- تولید خودکار کلید SSH اگر وجود نداشته باشد
- ریکانکت خودکار در صورت قطع تونل
- گرفتن پارامترها هم از CLI، هم YAML/ENV 
- API ساده برای Cloudflare (در cloudflare.py)
- قابلیت سفارشی‌سازی و توسعه حرفه‌ای
- مناسب اسکریپت‌ها و اتوماسیون DevOps

---

## مثال بارگذاری کانفیگ از yaml

```python
from tunnelmate.config import load_config

config = load_config("tunnels.yaml")
print(config)
```

---

## بروزرسانی رکورد DNS کلودفلر

```python
from tunnelmate.cloudflare import update_cname

resp = update_cname(zone_id, record_id, api_token, subdomain, target)
print(resp)
```

---

## ساختار پوشه

```
ssh_tunneler/
  core.py         # هسته اجرای تونل SSH
  cli.py          # رابط خط فرمان
  config.py       # کانفیگ و لود خودکار از yaml/env
  cloudflare.py   # بروزرسانی رکورد کلودفل
  ssh_utils.py    # ابزار SSH (تولید کلید و ...)
  __init__.py
setup.py
README.md
```

---

👨🏻‍💻 توسعه‌دهنده: پارسا لکزیان  
🤖 طراحی معماری: Tara AI
