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

    @app.get("/tables")
    def tables():
        try:
            with engine.connect() as conn:
                # 獲取所有資料表
                result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
                
                # 獲取每個資料表的結構
                table_info = {}
                for table in tables:
                    desc_result = conn.execute(text(f"DESCRIBE {table}"))
                    columns = []
                    for row in desc_result.fetchall():
                        columns.append({
                            "field": row[0],
                            "type": row[1],
                            "null": row[2],
                            "key": row[3],
                            "default": row[4],
                            "extra": row[5]
                        })
                    table_info[table] = columns
                
                return jsonify({
                    "tables": tables,
                    "table_info": table_info,
                    "total_tables": len(tables)
                })
        except SQLAlchemyError as e:
            return jsonify(db=False, error=str(e.__class__.__name__)), 500

    @app.get("/db-info")
    def db_info():
        try:
            with engine.connect() as conn:
                # 資料庫基本資訊
                db_name_result = conn.execute(text("SELECT DATABASE()"))
                db_name = db_name_result.fetchone()[0]
                
                # 連線資訊
                version_result = conn.execute(text("SELECT VERSION()"))
                version = version_result.fetchone()[0]
                
                # 資料表數量
                tables_result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in tables_result.fetchall()]
                
                # 資料庫大小
                size_result = conn.execute(text(f"""
                    SELECT 
                        ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'DB Size in MB'
                    FROM information_schema.tables 
                    WHERE table_schema = '{db_name}'
                """))
                db_size = size_result.fetchone()[0] or 0
                
                return jsonify({
                    "database_name": db_name,
                    "version": version,
                    "tables_count": len(tables),
                    "tables": tables,
                    "database_size_mb": db_size,
                    "connection_info": {
                        "host": "localhost",
                        "user": "py-admin",
                        "database": "shop"
                    }
                })
        except SQLAlchemyError as e:
            return jsonify(db=False, error=str(e.__class__.__name__)), 500

    return app

app = create_app()
