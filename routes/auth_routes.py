from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from database.user_model import User
from flask import current_app
from utils.auth_decorators import logout_required

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
@logout_required
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Basic validation
        if not name or not email or not password:
            flash("All fields are required!", "error")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long!", "error")
            return render_template("signup.html")

        existing_user = User.find_by_email(current_app.config["DB"], email)
        if existing_user:
            flash("Email already registered!", "error")
            return render_template("signup.html")

        try:
            user = User(name, email, password)
            user.save(current_app.config["DB"])
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth_bp.login"))
        except Exception as e:
            flash("An error occurred while creating your account. Please try again.", "error")
            return render_template("signup.html")

    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required!", "error")
            return render_template("login.html")

        user = User.find_by_email(current_app.config["DB"], email)
        if user and User.verify_password(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password!", "error")
            return render_template("login.html")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("index"))