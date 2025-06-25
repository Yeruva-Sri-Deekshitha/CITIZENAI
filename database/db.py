from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv()

def init_db(app):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/citizenai")
    print(f"✅ Loaded MONGO_URI: {mongo_uri}")
    app.config["MONGO_URI"] = mongo_uri
    mongo = PyMongo(app)
    return mongo