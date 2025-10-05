# Cloudflare Origin SSL

將從 Cloudflare 下載的 Origin Server Certificate 與私鑰放置：

- /etc/ssl/cloudflare/origin.crt
- /etc/ssl/cloudflare/origin.key

Nginx 以此配合 Cloudflare 「Full (strict)」模式。
