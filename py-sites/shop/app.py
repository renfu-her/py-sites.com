from flask import Flask
from sqlalchemy import create_engine, text
import os

def get_engine():
    user = os.getenv('DB_USER')
    pwd = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'mariadb')
    port = os.getenv('DB_PORT', '3306')
    db   = os.getenv('DB_DATABASE', 'shop_db')
    charset = os.getenv('DB_CHARSET', 'utf8mb4')
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset={charset}"
    return create_engine(url, pool_pre_ping=True)

engine = get_engine()
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from shop!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
