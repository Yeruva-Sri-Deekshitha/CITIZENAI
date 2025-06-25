from flask import Blueprint, render_template, current_app
from utils.auth_decorators import login_required

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    db = current_app.db
    
    try:
        feedbacks = list(db.feedbacks.find().sort("timestamp", -1).limit(50))
        
        positive = db.feedbacks.count_documents({"sentiment": "Positive"})
        neutral = db.feedbacks.count_documents({"sentiment": "Neutral"})
        negative = db.feedbacks.count_documents({"sentiment": "Negative"})
        
        total_feedbacks = positive + neutral + negative
        
        return render_template("dashboard.html", 
                             positive=positive, 
                             neutral=neutral,
                             negative=negative, 
                             total_feedbacks=total_feedbacks,
                             feedbacks=feedbacks)
    except Exception as e:
        return render_template("dashboard.html", 
                             error="Unable to load dashboard data",
                             positive=0, neutral=0, negative=0, 
                             total_feedbacks=0, feedbacks=[])