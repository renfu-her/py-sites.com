CREATE DATABASE IF NOT EXISTS main_db       CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS shop_db       CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS web_primary_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'pyapp'@'%' IDENTIFIED BY '${APP_DB_PASSWORD}';

GRANT ALL PRIVILEGES ON main_db.*        TO 'pyapp'@'%';
GRANT ALL PRIVILEGES ON shop_db.*        TO 'pyapp'@'%';
GRANT ALL PRIVILEGES ON web_primary_db.* TO 'pyapp'@'%';

FLUSH PRIVILEGES;
