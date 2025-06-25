from flask import Flask, render_template
from database.db import init_db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# ✅ MongoDB setup (direct URI in db.py)
mongo = init_db(app)
app.mongo = mongo
app.db = mongo.db
app.config["DB"] = mongo.db  # Store db in config for blueprint access

# Routes
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.sentiment_routes import sentiment_bp
from routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp)
app.register_blueprint(sentiment_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Test MongoDB connection
@app.route("/ping-db")
def ping_db():
    if app.db is None:
        return "❌ DB is not connected"

    try:
        app.db.command("ping")
        return "✅ MongoDB connected!"
    except Exception as e:
        return f"❌ MongoDB command failed: {e}"

if __name__ == "__main__":
    app.run(debug=True)
