from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return f"py-sites.com: Hello from Flask via Nginx + Gunicorn + Cloudflare (Full Strict)!"

    @app.get("/healthz")
    def healthz():
        return jsonify(ok=True, app="py-sites.com")

    return app

app = create_app()
