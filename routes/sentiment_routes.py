from flask import Blueprint, request, session, redirect, url_for, current_app
from models.sentiment_model import analyze_sentiment
from utils.auth_decorators import login_required
from datetime import datetime

sentiment_bp = Blueprint("sentiment_bp", __name__)

@sentiment_bp.route("/sentiment", methods=["POST"])
@login_required
def sentiment():
    question = request.form.get("question", "")
    response = request.form.get("response", "")
    feedback = request.form.get("feedback", "").strip()

    if feedback:
        sentiment_result = analyze_sentiment(feedback)

        # Store in session to show in chat
        session["question"] = question
        session["response"] = response
        session["sentiment"] = sentiment_result

        # Save to MongoDB with user information
        try:
            current_app.db.feedbacks.insert_one({
                "user_id": session.get("user_id"),
                "user_name": session.get("user_name"),
                "question": question,
                "response": response,
                "feedback": feedback,
                "sentiment": sentiment_result,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            print(f"Error saving feedback: {e}")

    return redirect(url_for("chat_bp.chat"))