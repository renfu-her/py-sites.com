from flask import Flask
app = Flask(__name__)

@app.get("/")
def index():
    return "Hello from web-primary.py-sites.com 🚀"
