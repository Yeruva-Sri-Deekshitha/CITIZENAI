from flask import Blueprint, render_template, request, session
from models.chat_model import generate_response

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            response = generate_response(question)
            return render_template("chat.html", question=question, question_response=response)

    # Show after feedback submission
    question = session.pop("question", None)
    response = session.pop("response", None)
    sentiment = session.pop("sentiment", None)

    return render_template("chat.html", question=question, question_response=response, sentiment=sentiment)
