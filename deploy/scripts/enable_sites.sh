#!/usr/bin/env bash
set -euo pipefail
sudo cp /home/renfu/htdocs/py-sites/deploy/nginx/*.conf /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/py-sites.com.conf /etc/nginx/sites-enabled/py-sites.com.conf
sudo ln -sf /etc/nginx/sites-available/shop.py-sites.com.conf /etc/nginx/sites-enabled/shop.py-sites.com.conf
sudo ln -sf /etc/nginx/sites-available/web-primary.py-sites.com.conf /etc/nginx/sites-enabled/web-primary.py-sites.com.conf
sudo nginx -t && sudo systemctl reload nginx
echo "Nginx 站台啟用完成 ✅"
