import os
from flask import Flask
from sqlalchemy import create_engine, text

def create_app():
    app = Flask(__name__)

    db_user = os.getenv("DB_USER", "pyapp")
    db_pass = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "mariadb")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "web_primary_db")

    app.config["DB_URL"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(app.config["DB_URL"], pool_pre_ping=True)

    @app.get("/")
    def hello():
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS healthz (id INT PRIMARY KEY AUTO_INCREMENT, at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
            r = conn.execute(text("SELECT NOW() as now")).mappings().one()
        return {
            "app": os.getenv("HOSTNAME", "flask-app"),
            "db": db_name,
            "now": str(r["now"])
        }

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    return app

app = create_app()
