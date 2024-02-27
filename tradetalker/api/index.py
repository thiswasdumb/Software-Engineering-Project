"""Contains the Flask application to send data to the TradeTalker frontend."""

import os
import re
from collections.abc import Callable
from typing import Literal

from flask import Flask, jsonify, redirect, request, session, url_for
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from werkzeug.wrappers import Response

from database.db_schema import (
    Article,
    Company,
    User,
    UserNotificationRead,
    add_data,
    db,
)

ErrorHandlerCallable = Callable[..., Response]


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb:///tradetalkerdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"
db.init_app(app)  # Initializes the database connection
CORS(app, supports_credentials=True)  # Allows backend to communicate with JS frontend


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore [reportAttributeAccessIssue]


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    """Returns the user with the given ID."""
    return db.session.get(User, user_id)


reset = True
if reset:
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_data()

MAX_EMAIL_LENGTH = 100
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 200


@app.errorhandler(404)
def page_not_found(_: Exception) -> tuple[Response, Literal[404]]:
    """Returns a 404 error."""
    return redirect("http://localhost:3000/not-found"), 404


# Example of how to create a route and return JSON data from a function
@app.route("/api/example", methods=["GET"])
def example() -> Response:
    """Returns an example SQL query."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Redirecting to another route
@app.route("/api/redirect", methods=["GET"])
def red() -> Response:
    """Redirects to the TradeTalker frontend."""
    return redirect(url_for("home"), code=302)


# Redirecting to a new page
@app.route("/api/home", methods=["GET"])
def home() -> Response:
    """Returns the homepage."""
    success = request.args.get("success")
    string = ""
    if success:
        string = f"?success={success}"
    return redirect(f"http://localhost:3000/{string}", code=301)


@app.route("/api/signup", methods=["GET"])
def signup() -> Response:
    """Returns the signup page."""
    error = request.args.get("error")
    string = ""
    if error:
        string = f"?error={error}"
    return redirect(f"http://localhost:3000/signup{string}", code=301)


@app.route("/api/registration", methods=["GET", "POST"])
def registration() -> Response:
    """Signs up a user."""
    error = ""
    url = ""
    if current_user.is_authenticated:
        error = "You are already logged in."
        return redirect(url_for("dashboard", error=error), code=301)

    if request.method == "POST":
        if request.json is None:
            error = "Invalid request."
            return redirect(url_for("registration", error=error), code=301)
        email = request.json["email"]
        username = request.json["username"]
        password = request.json["password"]

        # Server-side validation of credentials
        if (
            not re.match(r"[^@]+@[^@]+\.[^@]+", email)
            or len(email) > MAX_EMAIL_LENGTH
            or not (MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH)
            or not (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH)
            or not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}", password)
        ):
            error = "Invalid credentials!"
            return redirect(url_for("registration", error=error))

        # Hash password for security
        password_hash = security.generate_password_hash(password)
        # Direct user to login page if they already have an account
        user = db.session.query(User).filter_by(Email=email).first()
        if user is not None:
            if user.Username == username and security.check_password_hash(
                user.Password,
                password,
            ):
                error = ""  # Error message will be handled in the frontend
                url = "login"
            else:
                error = "Email has already been taken."
                url = "signup"
            return jsonify({"url": url, "error": error})

        try:
            # Create a user with their credentials
            new_user = User(
                username,
                password_hash,
                email,
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:  # If user failed to add, rollback the transaction
            db.session.rollback()
            error = "Could not sign up."
            url = "signup"
            return jsonify({"url": url, "error": error})

        login_user(new_user)
        session["username"] = current_user.Username
        # (Call the verify email function here)
        url = "dashboard"
        return jsonify({"url": url})

    error = "Invalid request."
    url = "signup"

    return jsonify({"url": url, "error": error})


@app.route("/api/login", methods=["GET"])
def login() -> Response:
    """Returns the login page."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"), code=301)
    error = request.args.get("error")
    success = request.args.get("success")
    string = ""
    if error:
        string = f"?error={error}"
    if success:
        string = f"?success={success}"
    return redirect(f"http://localhost:3000/login{string}", code=301)


@app.route("/api/login_form", methods=["GET", "POST"])
def login_form() -> Response:
    """Logs in the user."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard", error="You are already logged in."))

    if request.method == "POST":
        if request.json is None:
            return jsonify({"error": "Invalid request."})
        username = request.json["username"]
        password = request.json["password"]

        user = User.query.filter_by(Username=username).first()
        if user is None or not security.check_password_hash(user.Password, password):
            return jsonify({"error": "Invalid username or password."})
        login_user(user)
        session["username"] = username
        return jsonify({"success": "Successfully logged in!"})
    return jsonify({"error": "Invalid request."})


@app.route("/api/forgot_password", methods=["GET"])
def forgot_password() -> Response:
    """Returns the forgot password page."""
    return redirect("http://localhost:3000/forgot_password", code=301)


@app.route("/api/search/<string:query>", methods=["GET"])
def search(query: str) -> Response:
    """Returns the search results."""
    articles = Article.query.filter(Article.Title.like(f"%{query}%")).all()
    companies = Company.query.filter(Company.CompanyName.like(f"%{query}%")).all()
    return jsonify({"articles": articles, "companies": companies})


@app.route("/api/dashboard", methods=["GET", "POST"])
@login_required
def dashboard() -> Response:
    """Returns the dashboard."""
    success = request.args.get("success")
    string = ""
    if success:
        string = f"?success={success}"
    return redirect(f"http://localhost:3000/dashboard{string}", code=301)


@app.route("/api/get_dashboard_data", methods=["GET"])
@login_required
def get_dashboard_data() -> Response:
    """Returns the user's dashboard data."""
    return jsonify(current_user.Username)


@app.route("/api/get_notifications", methods=["GET"])
@login_required
def get_notifications() -> Response:
    """Returns the user's notifications."""
    notifications = UserNotificationRead.query.filter_by(
        UserID=current_user.id,
    ).all()
    return jsonify(notifications)


@app.route("/api/get_notification_count", methods=["GET"])
@login_required
def get_notification_count() -> Response:
    """Returns the user's notification count."""
    notif_count = (
        UserNotificationRead.query.filter_by(UserID=current_user.id)
        .filter_by(IsRead=False)
        .count()
    )
    return jsonify(notif_count)


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile() -> Response:
    """Returns the user's profile."""
    return redirect("http://localhost:3000/profile", code=301)


@app.route("/api/get_profile_data", methods=["GET"])
@login_required
def get_profile_data() -> Response:
    """Returns the user's profile data."""
    return jsonify(current_user.Username)


@app.route("/api/logout")
def logout() -> Response:
    """Logs out the user."""
    if current_user.is_authenticated:
        session.clear()
        logout_user()
        return redirect(url_for("home", success="Successfully logged out!"), code=301)
    return redirect(url_for("login", error="You are not logged in."), code=301)


@app.route("/delete_user", methods=["POST"])
def delete_user() -> Response:
    """Deletes the user."""
    if current_user.is_authenticated:
        session.clear()
        logout_user()
        db.session.delete(current_user)
        db.session.commit()
        return redirect(
            url_for("home", success="Successfully deleted account!"),
            code=301,
        )
    return redirect(url_for("login", error="You are not logged in."))


if __name__ == "__main__":
    app.run(debug=os.environ["ENV"] == "dev", port=8080)
