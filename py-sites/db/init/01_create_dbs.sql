CREATE DATABASE IF NOT EXISTS shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS web_primary_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用 .env 中的 DB_USER（預先由 entrypoint 建立）
GRANT ALL PRIVILEGES ON shop_db.* TO 'py-admin'@'%';
GRANT ALL PRIVILEGES ON web_primary_db.* TO 'py-admin'@'%';
FLUSH PRIVILEGES;
