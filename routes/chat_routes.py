from flask import Blueprint, render_template, request, session
from models.chat_model import generate_response
from utils.auth_decorators import login_required

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            response = generate_response(question)
            return render_template("chat.html", question=question, question_response=response)
        else:
            return render_template("chat.html", error="Please enter a question.")

    # Show after feedback submission
    question = session.pop("question", None)
    response = session.pop("response", None)
    sentiment = session.pop("sentiment", None)

    return render_template("chat.html", question=question, question_response=response, sentiment=sentiment)