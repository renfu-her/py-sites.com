# app.py  ─ 最小可用 Flask，不連 DB
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/healthz")
def healthz():
    # 給反向代理 / Cloudflare 用，不動任何外部資源
    return {"ok": True}

@app.get("/")
def index():
    # 回一些環境資訊，方便你辨識是哪個服務
    return jsonify({
        "ok": True,
        "service": os.getenv("APP_NAME", os.getenv("DB_NAME", "app")),  # 可用 APP_NAME 或沿用 DB_NAME 當識別
        "hostname": os.getenv("HOSTNAME", "flask-app"),
        "db_enabled": False
    })

