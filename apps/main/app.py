import os
import socket
from urllib.parse import quote_plus
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# ---- 讀環境變數 ----
DB_USER = os.getenv("DB_USER", "py-app")
DB_PASS = os.getenv("DB_PASSWORD", "py-password")
DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "main_db")
CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", "10"))

# 組連線字串（pymysql）
DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# 建 engine
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=5,
    connect_args={"connect_timeout": CONNECT_TIMEOUT},
)

def mask(s: str, keep: int = 1) -> str:
    """遮罩字串（只保留前 keep 個字元）"""
    if not s:
        return ""
    return s[:keep] + "*****"

def safe_db_url() -> str:
    """產生遮罩後可顯示的 DB URL（不外洩密碼）"""
    return f"mysql+pymysql://{DB_USER}:{mask(DB_PASS_RAW)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 啟動時把已遮罩的 DB 連線印到 log
app.logger.info("DB connect (masked): %s", safe_db_url())

@app.get("/healthz")
def healthz():
    # 不動 DB，給反向代理/CF 健康檢查
    return {"ok": True}

@app.get("/dbinfo")
def dbinfo():
    """回傳目前 DB 連線資訊 + 即時健康檢查"""
    # 1) DNS 解析
    dns_ok = True
    db_ip = None
    dns_error = None
    try:
        db_ip = socket.gethostbyname(DB_HOST)
    except Exception as e:
        dns_ok = False
        dns_error = str(e)

    # 2) 連線測試（SELECT VERSION()/DATABASE()）
    conn_ok = True
    details = {}
    error = None
    try:
        with engine.connect() as conn:
            ver = conn.execute(text("SELECT VERSION() AS v")).mappings().one()["v"]
            curdb = conn.execute(text("SELECT DATABASE() AS d")).mappings().one()["d"]
            # 簡單 query 測速
            conn.execute(text("SELECT 1"))
            details = {"version": ver, "current_db": str(curdb)}
    except SQLAlchemyError as e:
        app.logger.exception("DB connection test failed")
        conn_ok = False
        error = f"{e.__class__.__name__}: {e}"

    return jsonify({
        "config": {
            "url_masked": safe_db_url(),
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "db_name": DB_NAME,
            "timeout_sec": CONNECT_TIMEOUT,
        },
        "dns": {"ok": dns_ok, "ip": db_ip, "error": dns_error},
        "connection": {"ok": conn_ok, "error": error, "details": details},
    })

@app.get("/")
def index():
    """正式路由：會碰 DB，失敗就 500 + 短錯訊"""
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS healthz (
                  id INT PRIMARY KEY AUTO_INCREMENT,
                  at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            r = conn.execute(text("SELECT NOW() AS now")).mappings().one()
        return {
            "ok": True,
            "app": os.getenv("HOSTNAME", "main"),
            "db": DB_NAME,
            "now": str(r["now"])
        }
    except SQLAlchemyError as e:
        app.logger.exception("DB error on /")
        return jsonify({"ok": False, "error": "db_unavailable", "detail": e.__class__.__name__}), 500
