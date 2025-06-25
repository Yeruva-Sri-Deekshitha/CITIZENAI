from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from database.user_model import User
from flask import current_app

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.find_by_email(current_app.config["DB"], email)
        if existing_user:
            flash("Email already registered!", "error")
            return redirect(url_for("auth_bp.signup"))

        user = User(name, email, password)
        user.save(current_app.config["DB"])

        flash("Account created successfully!", "success")
        return redirect(url_for("auth_bp.login"))

    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.find_by_email(current_app.config["DB"], email)
        if user and User.verify_password(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for("auth_bp.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth_bp.login"))
