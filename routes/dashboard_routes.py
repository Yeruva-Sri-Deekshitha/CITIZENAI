from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    db = current_app.db
    feedbacks = list(db.feedbacks.find())

    positive = db.feedbacks.count_documents({"sentiment": "Positive"})
    neutral = db.feedbacks.count_documents({"sentiment": "Neutral"})
    negative = db.feedbacks.count_documents({"sentiment": "Negative"})

    return render_template("dashboard.html", positive=positive, neutral=neutral,
                           negative=negative, feedbacks=feedbacks)
