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

## MariaDB 資料庫設定

### 🧱 一、安裝 MariaDB Server
```bash
sudo apt update
sudo apt install -y mariadb-server mariadb-client
```

啟動並設定開機自動啟動：
```bash
sudo systemctl enable --now mariadb
sudo systemctl status mariadb
```

### 🧹 二、初始化安全設定（建議）
這會讓你設定 root 密碼、移除匿名帳號、關掉遠端 root 登入等。
```bash
sudo mysql_secure_installation
```

如果跳出 command not found，請執行：
```bash
sudo mariadb-secure-installation
```

### 🧠 三、建立資料庫與使用者（對應 shop）
登入 MariaDB：
```bash
sudo mariadb
```

進入後執行以下 SQL：
```sql
CREATE DATABASE shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'py-admin'@'localhost' IDENTIFIED BY 'py-password';
GRANT ALL PRIVILEGES ON shop.* TO 'py-admin'@'localhost';

FLUSH PRIVILEGES;
EXIT;
```

> 💡 如果你只會從本機（Flask 伺服器）連線，@'127.0.0.1' 已經足夠。  
> 如果之後要讓別台伺服器連，可以改 @'%'（但要搭配防火牆限制）。

### 🧪 四、測試連線是否 OK
```bash
mysql -u py-admin -p'py-password' -h 127.0.0.1 -P 3306 -e "SELECT 1;"
```

應該會印出：
```
+---+
| 1 |
+---+
| 1 |
+---+
```

### ⚙️ 五、重啟 Flask shop 後端並驗證
確保 .env 已設定：
```bash
cat ~/htdocs/py-sites/shop/.env
```

內容：
```
DB_USER=py-admin
DB_PASSWORD=py-password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=shop
```

重新啟動後端：
```bash
sudo systemctl restart gunicorn-shop
sudo systemctl status gunicorn-shop --no-pager -l
```

### 🧩 六、測試 DB 連線
方式一：透過內部 socket 直測
```bash
curl -sS http://unix:/run/py-sites/gunicorn-shop.sock:/dbz
```

方式二：透過 Nginx + Cloudflare
```bash
curl -sk https://shop.py-sites.com/dbz -H "Host: shop.py-sites.com"
```

成功的話會看到：
```json
{"db": true}
```

### 🪄 小補充（防踩坑）
| 問題 | 原因 | 解法 |
|------|------|------|
| 連不上 DB (Connection refused) | MariaDB 沒開 / 被防火牆擋 | `sudo systemctl status mariadb` / `sudo ufw allow 3306` |
| Access denied for user 'py-admin' | 權限錯誤 / 用錯 host | 確認 `GRANT ... TO 'py-admin'@'127.0.0.1'` |
| Flask 起不來 | 缺 SQLAlchemy | 重新跑 `pip install -r requirements.txt` |

> 若你先前要移除 Docker / MariaDB，與本部署無衝突。本方案純系統服務（Nginx + Gunicorn）。
