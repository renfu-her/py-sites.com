# apps/main/app.py
import os
from urllib.parse import quote_plus
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

db_user = os.getenv("DB_USER", "py-app")
db_pass = quote_plus(os.getenv("DB_PASSWORD", ""))  # 密碼安全編碼
db_host = os.getenv("DB_HOST", "mariadb")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "main_db")

db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=1800)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/")
def index():
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS healthz (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            r = conn.execute(text("SELECT NOW() AS now")).mappings().one()
        return {"ok": True, "app": os.getenv("HOSTNAME","main"), "db": db_name, "now": str(r["now"])}
    except SQLAlchemyError as e:
        app.logger.exception("DB error")
        return jsonify({"ok": False, "error": "db_unavailable", "detail": e.__class__.__name__}), 500
