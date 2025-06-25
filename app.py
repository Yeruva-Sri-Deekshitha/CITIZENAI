from flask import Flask, render_template, session, redirect, url_for
from database.db import init_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Generate a simple secret key - you can change this
app.secret_key = os.getenv("SECRET_KEY", "citizenai-secret-key-change-this-in-production")

# MongoDB setup
mongo = init_db(app)
app.mongo = mongo
app.db = mongo.db
app.config["DB"] = mongo.db

# Import and register blueprints
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
    if 'user_id' not in session:
        return render_template("landing.html")
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Test MongoDB connection
@app.route("/ping-db")
def ping_db():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    if app.db is None:
        return "❌ DB is not connected"

    try:
        app.db.command("ping")
        return "✅ MongoDB connected!"
    except Exception as e:
        return f"❌ MongoDB command failed: {e}"

# Context processor to make user info available in all templates
@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    return dict(current_user_id=user_id, current_user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)