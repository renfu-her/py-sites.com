from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def create_app():
    app = Flask(__name__)
    db_uri = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://py-admin:py-password@127.0.0.1:3306/shop?charset=utf8mb4",
    )
    # 避免 localhost 走 socket，強制 TCP
    db_uri = db_uri.replace("@localhost/", "@127.0.0.1/")
    if "charset=" not in db_uri:
        sep = "&" if "?" in db_uri else "?"
        db_uri = f"{db_uri}{sep}charset=utf8mb4"

    engine = create_engine(
        db_uri,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=5,
        future=True,
    )

    @app.get("/")
    def index():
        return "shop.py-sites.com: Flask + Gunicorn + Nginx + Cloudflare + MariaDB ✅"

    @app.get("/healthz")
    def healthz():
        return jsonify(ok=True, app="shop.py-sites.com")

    @app.get("/dbz")
    def dbz():
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return jsonify(db=True)
        except SQLAlchemyError as e:
            return jsonify(db=False, error=str(e.__class__.__name__)), 500

    return app

app = create_app()
