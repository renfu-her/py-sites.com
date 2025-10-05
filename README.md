# py-sites — Flask x Nginx x Cloudflare (Origin Cert)

此範例為三個 Flask 站點：
- **py-sites.com** (`main/`)
- **shop.py-sites.com** (`shop/`)
- **web-primary.py-sites.com** (`web_primary/`)

部署策略：Cloudflare → Nginx (TLS 使用 Cloudflare Origin Cert) → Gunicorn (Unix socket) → Flask。

## 目錄結構（預期部署在 `/home/renfu/htdocs/py-sites`）

```
py-sites/
├── main/
│   ├── app.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── gunicorn.conf.py
│   └── .env.example
├── shop/
│   ├── app.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── gunicorn.conf.py
│   └── .env.example
├── web_primary/
│   ├── app.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── gunicorn.conf.py
│   └── .env.example
├── shared/
│   └── logs/               # 放 Nginx / App 日誌（可自訂）
└── deploy/
    ├── nginx/
    │   ├── py-sites.com.conf
    │   ├── shop.py-sites.com.conf
    │   └── web-primary.py-sites.com.conf
    ├── systemd/
    │   ├── gunicorn-main.service
    │   ├── gunicorn-shop.service
    │   └── gunicorn-web-primary.service
    ├── ssl/
    │   └── README-ssl.txt
    └── scripts/
        ├── setup_venv.sh
        ├── enable_sites.sh
        └── test_health.sh
```

## 快速安裝步驟（Ubuntu 22.04/24.04）

1) 安裝系統套件：
```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev build-essential nginx
```

2) 佈署專案：
```bash
sudo mkdir -p /home/renfu/htdocs/py-sites
sudo chown -R $USER:www-data /home/renfu/htdocs/py-sites
# 將本壓縮包解開至 /home/renfu/htdocs/py-sites 上層後移動到該路徑
# 例如：tar -xzf ~/Downloads/py-sites-starter.tar.gz -C ~ && mv ~/py-sites /home/renfu/htdocs/py-sites
```

3) 建立三個 venv 並安裝：
```bash
cd /home/renfu/htdocs/py-sites
bash deploy/scripts/setup_venv.sh
```

4) 放置 Cloudflare Origin Cert（Full (strict)）：
```bash
sudo mkdir -p /etc/ssl/cloudflare
# 將你的 origin.crt 與 origin.key 放入：
#   /etc/ssl/cloudflare/origin.crt
#   /etc/ssl/cloudflare/origin.key
sudo chmod 600 /etc/ssl/cloudflare/origin.key
sudo chown root:root /etc/ssl/cloudflare/origin.key /etc/ssl/cloudflare/origin.crt
```

5) 啟用 systemd 服務（Gunicorn 三個站點）：
```bash
sudo cp /home/renfu/htdocs/py-sites/deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-main gunicorn-shop gunicorn-web-primary
systemctl status gunicorn-main --no-pager -l
```

6) 啟用 Nginx 站台：
```bash
sudo cp /home/renfu/htdocs/py-sites/deploy/nginx/*.conf /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/py-sites.com.conf /etc/nginx/sites-enabled/py-sites.com.conf
sudo ln -sf /etc/nginx/sites-available/shop.py-sites.com.conf /etc/nginx/sites-enabled/shop.py-sites.com.conf
sudo ln -sf /etc/nginx/sites-available/web-primary.py-sites.com.conf /etc/nginx/sites-enabled/web-primary.py-sites.com.conf
sudo nginx -t && sudo systemctl reload nginx
```

7) 健康檢查：
```bash
bash deploy/scripts/test_health.sh
# 或透過瀏覽器確認 https://py-sites.com / https://shop.py-sites.com / https://web-primary.py-sites.com
```

> 若你先前要移除 Docker / MariaDB，與本部署無衝突。本方案純系統服務（Nginx + Gunicorn）。
