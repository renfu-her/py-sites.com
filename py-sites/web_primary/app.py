from flask import Flask
from sqlalchemy import create_engine, text
import os

def create_app():
    app = Flask(__name__)

    # 讀 .env（可用 python-dotenv 的自動載入，或手動組）
    db_url = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost/py_sites_main?charset=utf8mb4")
    engine = create_engine(db_url, pool_pre_ping=True, future=True)

    @app.get("/")
    def index():
        # Demo: 讀 DB 現在時間
        with engine.connect() as conn:
            now = conn.execute(text("SELECT NOW()")).scalar()
        return f"web-primary.py-sites.com OK. DB NOW: {now}"

    return app

# 給 gunicorn 使用
app = create_app()
