"""Contains the Flask application to send data to the TradeTalker frontend."""

import os
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Mail, Message
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from werkzeug.wrappers import Response

from database.db_schema import (
    Article,
    ArticleComment,
    Bookmark,
    Company,
    Faq,
    Follow,
    LikeTable,
    Notification,
    User,
    UserNotificationRead,
    UserQuestion,
    add_base_company_data,
    add_data,
    db,
    get_articles_from_news_api,
    get_recommendation_system_info,
    set_all_companies_predicted_price,
)
from database.recommendation_system import RecommendationSystem
from database.search_component import ArticleSearch

app = Flask(__name__)
app.config.from_object(__name__)

if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

IMAGE_FOLDER = "../public/"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "tradetalks202@gmail.com"
app.config["MAIL_PASSWORD"] = "pgun undn yvpf doyd"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb:///tradetalkerdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["MAIL_SUPPRESS_SEND"] = False

mail = Mail(app)
db.init_app(app)  # Initializes the database connection

CORS(
    app,
    origins="http://localhost:3000",
    supports_credentials=True,
)  # Allows backend to communicate with JS frontend


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    """Returns the user with the given ID."""
    return db.session.get(User, user_id)


reset = True  # Set to False to keep the database data on restart
if reset:
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_base_company_data()
        add_data()
        get_articles_from_news_api()
        set_all_companies_predicted_price()


MAX_EMAIL_LENGTH = 100
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 200
MIN_COMMENT_LENGTH = 1
MAX_COMMENT_LENGTH = 10000


@app.errorhandler(404)
def page_not_found(_: Exception) -> tuple[Response, Literal[404]]:
    """Returns a 404 error."""
    return redirect("http://localhost:3000/not-found"), 404


# Example of how to create a route and return JSON data from a function
@app.route("/api/home_articles", methods=["GET"])
def example() -> Response:
    """Returns an example SQL query."""
    # Get the newest 3 articles
    articles = (
        db.session.execute(
            db.select(Article).order_by(desc(Article.PublicationDate)).limit(3),
        )
        .scalars()
        .all()
    )
    articles_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
            "score": article.PredictionScore,
            "comments": db.session.execute(
                db.select(db.func.count())
                .select_from(ArticleComment)
                .filter(ArticleComment.ArticleID == article.ArticleID),
            ).scalar(),
        }
        for article in articles
    ]
    return jsonify(articles_list)


@app.route("/api/home", methods=["GET"])
def home() -> Response:
    """Returns the homepage."""
    success = request.args.get("success")
    string = ""
    if success:
        string = f"?success={success}"
    return redirect(f"http://localhost:3000/{string}", code=301)


# Redirecting to another route
@app.route("/api/redirect", methods=["GET"])
def red() -> Response:
    """Redirects to the TradeTalk frontend."""
    return redirect(url_for("home"), code=302)


# ----------------- User authentication routes -----------------


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
        or not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        )
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
        db.session.commit()  # Commit the transaction
    except IntegrityError:  # If user failed to add, rollback the transaction
        db.session.rollback()
        return jsonify({"url": "signup", "error": "Could not sign up."})

    login_user(new_user)
    session["username"] = current_user.Username
    # (Call the verify email function here)
    return send_verify_email(new_user)


# Sends verification email to a User during signup
def send_verify_email(user: User) -> Response:
    """Sends a verification email to the user."""
    if current_user.IsVerified:
        return jsonify({"url": "dashboard", "error": "You are already verified."})

    token = User.get_reset_token(user)
    msg = Message(
        subject="Verify your TradeTalk account",
        sender=("TradeTalk", "tradetalk-admin@example.com"),
        recipients=[current_user.Email],
    )
    msg.html = render_template("verify_message.html", token=token)
    # Attach an image to the header
    with Path(IMAGE_FOLDER + "images/logo.png").open("rb") as file:
        msg.attach(
            "logo.png",
            "image/png",
            file.read(),
            "inline",
            headers=[["Content-ID", "<MyImage>"]],
        )
    msg.sender = "TradeTalk <tradetalk-admin@example.com>"
    mail.send(msg)
    return jsonify({"url": "dashboard", "success": "Verification email sent."})


@app.route("/api/verify/<string:token>", methods=["GET", "POST"])
@login_required
def verify(token: str) -> Response:
    """Verifies the user's email."""
    if current_user.IsVerified:
        return redirect(url_for("dashboard", error="You are already verified."))
    if current_user.id == User.verify_reset_token(token):
        try:
            current_user.IsVerified = 1  # User is now confirmed
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("home", error="Could not verify email."))
        return redirect(url_for("dashboard", success="Email verified!"))
    return redirect(url_for("home", error="Invalid or expired token."))


@app.route("/api/login", methods=["GET"])
def login() -> Response:
    """Returns the login page."""
    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard", error="You are already logged in."),
            code=301,
        )
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
        # Select the user with the given username
        user = (
            db.session.execute(db.select(User).filter_by(Username=username))
            .scalars()
            .first()
        )
        # Get the password of the user
        if user is None or not security.check_password_hash(user.Password, password):
            return jsonify({"error": "Invalid username or password."})
        login_user(user)
        session["username"] = username
        return jsonify({"success": "Successfully logged in!"})
    return jsonify({"error": "Invalid request."})


@app.route("/api/forgot_password", methods=["GET", "POST"])
def forgot_password() -> Response:
    """Sends a password reset email to the user."""
    if request.json is None:
        error = "Invalid request."
        return redirect(url_for("registration", error=error), code=301)
    email = request.json["email"]
    user = db.session.execute(db.select(User).filter_by(Email=email)).scalar()
    if user is None:
        return jsonify({"error": "Email does not exist. Please sign up."})
    token = User.get_reset_token(user)
    msg = Message(
        subject="Reset your TradeTalk account password",
        sender=("TradeTalk", "tradetalk-admin@example.com"),
        recipients=[user.Email],
    )
    msg.html = render_template("reset_password.html", token=token)
    # Attach an image to the header
    with Path(IMAGE_FOLDER + "images/logo.png").open("rb") as file:
        msg.attach(
            "logo.png",
            "image/png",
            file.read(),
            "inline",
            headers=[["Content-ID", "<MyImage>"]],
        )
    msg.sender = "TradeTalk <tradetalk-admin@example.com>"
    mail.send(msg)
    return jsonify({"success": "Password reset email sent."})


@app.route("/api/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password_page(token: str) -> Response:
    """Returns the reset password page."""
    return redirect(f"http://localhost:3000/reset-password/{token}", code=301)


@app.route("/api/submit_reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token: str) -> Response:
    """Resets the user's password."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    password = request.json["password"]
    password_repeat = request.json["password_repeat"]
    user_id = User.verify_reset_token(token)
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    if user is None:
        return jsonify({"error": "Invalid or expired token."})
    if not (
        MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH
    ) or not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        password,
    ):
        return jsonify({"error": "Invalid password."})
    if password != password_repeat:
        return jsonify({"error": "Passwords do not match."})
    if security.check_password_hash(user.Password, password):
        return jsonify(
            {"error": "New password cannot be the same as the old password."},
        )
    user.Password = security.generate_password_hash(password)
    db.session.commit()
    if not current_user.is_authenticated:
        login_user(user)
    return jsonify({"success": "Password reset successfully!"})


# ----------------- Search routes -----------------


@app.route("/api/search/<string:query>", methods=["GET"])
def search(query: str | None) -> Response:
    """Returns the search results."""
    # Search for articles and companies with the given query
    articles = (
        db.session.execute(db.select(Article).filter(Article.Title.like(f"%{query}%")))
        .scalars()
        .all()
    )

    all_articles = db.session.execute(db.select(Article)).scalars().all()

    key_article_ids = ArticleSearch(all_articles).search(query)
    key_articles = (
        db.session.execute(
            db.select(Article).filter(
                (Article.ArticleID.in_(key_article_ids[0]))
                | (Article.ArticleID.in_(key_article_ids[1]))
                | (Article.ArticleID.in_(key_article_ids[2]))
                | (Article.ArticleID.in_(key_article_ids[3]))
                | (Article.ArticleID.in_(key_article_ids[4])),
            ),
        )
        .scalars()
        .all()
    )

    companies = (
        db.session.execute(
            db.select(Company)
            .filter(
                Company.CompanyName.like(f"%{query}%")
                | Company.StockSymbol.like(f"%{query}%"),
            )
            .order_by(Company.StockPrice.desc()),
        )
        .scalars()
        .all()
    )
    articles_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
        }
        for article in articles
    ]

    article_keywords_list = [
        {
            "id": key_article.ArticleID,
            "title": key_article.Title,
            "date": key_article.PublicationDate,
            "summary": key_article.Summary,
        }
        for key_article in key_articles
    ]

    companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "stock_price": company.StockPrice,
            "symbol": company.StockSymbol,
            "industry": company.Industry,
        }
        for company in companies
    ]
    return jsonify(
        {
            "article_titles": articles_list,
            "article_keywords": article_keywords_list,
            "companies": companies_list,
        },
    )


# ----------------- Dashboard routes -----------------


@app.route("/api/check_verified", methods=["GET"])
@login_required
def check_verified() -> Response:
    """Returns whether the user is verified."""
    return jsonify({"verified": current_user.IsVerified})


@app.route("/api/dashboard", methods=["GET", "POST"])
@login_required
def dashboard() -> Response:
    """Returns the dashboard."""
    success = request.args.get("success")
    error = request.args.get("error")
    string = ""
    if success:
        string = f"?success={success}"
    if error:
        string = f"?error={error}"
    return redirect(f"http://localhost:3000/dashboard{string}", code=301)


@app.route("/api/get_dashboard_data", methods=["GET"])
def get_dashboard_data() -> Response:
    """Returns the user's dashboard data."""
    if current_user.is_authenticated:  # Currently buggy with @login_required
        return jsonify({"username": "Welcome, " + current_user.Username})
    return jsonify({"error": "You are not logged in."})


@app.route("/api/get_followed_companies", methods=["GET"])
@login_required
def get_followed_companies() -> Response:
    """Returns the user's followed companies."""
    followed_companies = (
        db.session.execute(
            db.select(Company)
            .join(Follow, Company.CompanyID == Follow.CompanyID)
            .filter(Follow.UserID == current_user.id)
            .order_by(desc(Follow.FollowDate)),
        )
        .scalars()
        .all()
    )
    followed_companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "symbol": company.StockSymbol,
        }
        for company in followed_companies
    ]
    return jsonify(followed_companies_list)


@app.route("/api/get_recommended_articles", methods=["GET"])
@login_required
def get_recommended_articles() -> Response:
    """Returns 3 articles linked to companies the user follows."""
    # Get the 3 most recent articles from followed companies that the user has not liked
    followed_company_ids = (
        db.session.execute(
            db.select(Follow.CompanyID).filter(Follow.UserID == current_user.id),
        )
        .scalars()
        .all()
    )
    recommended_articles = (
        db.session.execute(
            db.select(Article)
            .filter(Article.CompanyID.in_(followed_company_ids))
            .filter(
                ~Article.ArticleID.in_(
                    db.select(LikeTable.ArticleID).filter(
                        LikeTable.UserID == current_user.id,
                    ),
                ),
            )
            .order_by(desc(Article.PublicationDate))
            .limit(3),
        )
        .scalars()
        .all()
    )
    recommended_articles_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
            "score": article.PredictionScore,
        }
        for article in recommended_articles
    ]
    return jsonify(recommended_articles_list)


@app.route("/api/get_recommended_companies", methods=["GET"])
@login_required
def get_recommended_companies() -> Response:
    """Returns the user's recommended companies."""
    # Right now this only selects 3 random companies that the user is not following
    rec_company_ids = RecommendationSystem(
        get_recommendation_system_info(current_user.id),
    ).recommend()
    rec_companies = [
        db.session.execute(
            db.select(Company).filter(Company.CompanyID == company_id),
        ).scalar()
        for company_id in rec_company_ids
    ]
    rec_companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "symbol": company.StockSymbol,
        }
        for company in rec_companies
    ]
    return jsonify(rec_companies_list)


@app.route("/api/get_week_newsfeed", methods=["GET"])
@login_required
def get_week_newsfeed() -> Response:
    """Returns the 5 most recent articles from the followed companies in the last
    week.
    """
    # Get the 5 most recent articles from the followed companies in the last week
    newsfeed = (
        db.session.execute(
            db.select(Article)
            .filter(
                Article.PublicationDate >= datetime.now(UTC) - timedelta(days=7),
            )
            .order_by(desc(Article.PublicationDate))
            .limit(5),
        )
        .scalars()
        .all()
    )
    newsfeed_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
            "score": article.PredictionScore,
        }
        for article in newsfeed
    ]
    return jsonify(newsfeed_list)


@app.route("/api/get_week_newsfeed_full", methods=["GET"])
@login_required
def get_week_newsfeed_full() -> Response:
    """Returns the full list of articles from the followed companies in the last
    week.
    """
    # Get the full list of articles from the followed companies in the last week
    newsfeed = (
        db.session.execute(
            db.select(Article)
            .filter(
                Article.PublicationDate >= datetime.now(UTC) - timedelta(days=7),
            )
            .order_by(desc(Article.PublicationDate)),
        )
        .scalars()
        .all()
    )
    newsfeed_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
            "score": article.PredictionScore,
        }
        for article in newsfeed
    ]
    return jsonify(newsfeed_list)


# ----------------- Stocks routes -----------------


@app.route("/api/get_stock_trends", methods=["GET"])
def get_stock_trends() -> Response:
    """Returns the stock trends."""
    # Get the stock trends
    stock_trends = (
        db.session.execute(
            db.select(Company).order_by(Company.PredictedStockPrice.desc()).limit(25),
        )
        .scalars()
        .all()
    )
    stock_trends_list = [
        {
            "company_id": stock_trend.CompanyID,
            "company_name": stock_trend.CompanyName,
            "symbol": stock_trend.StockSymbol,
            "stock_price": stock_trend.StockPrice,
            "predicted_stock_price": stock_trend.PredictedStockPrice,
            "stock_variance": stock_trend.StockVariance,
        }
        for stock_trend in stock_trends
    ]
    return jsonify(stock_trends_list)


@app.route("/api/get_most_positive_leaderboard", methods=["GET"])
def get_most_positive_leaderboard() -> Response:
    """Returns the leaderboard of the most positive companies by articles."""
    # Get the leaderboard of companies sorted by descending average sentiment score of
    # articles that mention them
    companies = (
        db.session.execute(
            db.select(Company, db.func.avg(Article.PredictionScore).label("avg_score"))
            .join(Article)
            .group_by(Company.CompanyID)
            .order_by(db.func.avg(Article.PredictionScore).desc()),
        )
        .scalars()
        .all()
    )
    leaderboard_list = [
        {
            "company_id": company.CompanyID,
            "company_name": company.CompanyName,
            "company_symbol": company.StockSymbol,
            "stock_price": company.StockPrice,
        }
        for company in companies
    ]
    return jsonify(leaderboard_list)


@app.route("/api/get_top_stocks_leaderboard", methods=["GET"])
def get_top_stocks_leaderboard() -> Response:
    """Returns the leaderboard of companies with the highest stock price."""
    # Get the leaderboard
    leaderboard = (
        db.session.execute(db.select(Company).order_by(Company.StockPrice.desc()))
        .scalars()
        .all()
    )
    leaderboard_list = [
        {
            "company_id": company.CompanyID,
            "company_name": company.CompanyName,
            "company_symbol": company.StockSymbol,
            "stock_price": company.StockPrice,
        }
        for company in leaderboard
    ]
    return jsonify(leaderboard_list)


# ----------------- Article routes -----------------


@app.route("/api/get_article/<string:article_id>", methods=["GET"])
def get_article(article_id: str) -> Response:
    """Returns the article."""
    # Get the article with the given ID
    article = (
        db.session.execute(db.select(Article).filter_by(ArticleID=article_id))
        .scalars()
        .first()
    )
    if article is not None:
        # Get the company name of the article using the company ID
        company_name = (
            db.session.execute(
                db.select(Company.CompanyName).filter_by(CompanyID=article.CompanyID),
            )
            .scalars()
            .first()
        )
        article_json = {
            "company_name": company_name,
            "company_id": article.CompanyID,
            "title": article.Title,
            "content": article.Content,
            "publication_date": article.PublicationDate,
            "url": article.URL,
            "source": "src",
            "summary": article.Summary,
            "prediction_score": article.PredictionScore,
        }
        return jsonify(article_json)
    return jsonify({"error": "Article not found."})


@app.route("/api/article/<string:article_id>/comments", methods=["GET"])
def get_article_comments(article_id: str) -> Response:
    """Returns the article comments."""
    # Get the article comments with the given article ID
    comments = (
        db.session.execute(
            db.select(ArticleComment)
            .join(User, ArticleComment.UserID == User.id)
            .filter(ArticleComment.ArticleID == article_id)
            .order_by(ArticleComment.Time.desc()),
        )
        .scalars()
        .all()
    )

    comments_list = [
        {
            "id": comment.CommentID,
            "username": db.session.execute(
                db.select(User.Username).filter_by(
                    id=comment.UserID,
                ),  # Include username
            ).scalar(),
            "content": comment.Content,
            "time": comment.Time,
            "parent_id": comment.ParentCommentID,
        }
        for comment in comments
    ]
    return jsonify(comments_list)


@app.route("/api/add_article_comment/<string:article_id>", methods=["GET", "POST"])
@login_required
def add_article_comment(article_id: str) -> Response:
    """Adds a comment to the article."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    comment = request.json["comment"]
    if len(comment) < MIN_COMMENT_LENGTH or len(comment) > MAX_COMMENT_LENGTH:
        return jsonify({"error": "Comment must be between 1 and 10000 characters."})
    try:
        # Add a comment to the article with the given ID
        new_comment = ArticleComment(
            current_user.id,
            article_id,
            comment,
            None,
        )
        db.session.add(new_comment)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not add comment."})
    return jsonify({"success": "Successfully added comment."})


@app.route("/api/delete_article_comment/<string:comment_id>", methods=["GET"])
@login_required
def delete_article_comment(comment_id: str) -> Response:
    """Deletes the article comment."""
    try:
        # Delete the article comment with the given ID
        db.session.execute(
            db.delete(ArticleComment).filter(
                ArticleComment.CommentID == comment_id,
                ArticleComment.UserID == current_user.id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not delete comment."})
    return jsonify({"success": "Successfully deleted comment."})


@app.route(
    "/api/add_article_reply/<string:article_id>/<string:comment_id>",
    methods=["GET", "POST"],
)
@login_required
def add_article_reply(article_id: str, comment_id: str) -> Response:
    """Adds a reply to the article comment."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    reply = request.json["reply"]
    try:
        # Add a reply to the comment with the given ID
        new_reply = ArticleComment(
            current_user.id,
            article_id,
            reply,
            comment_id,
        )
        db.session.add(new_reply)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not add reply."})
    return jsonify({"success": "Successfully added reply."})


@app.route("/api/get_article_like_status/<string:article_id>", methods=["GET"])
@login_required
def get_article_like_status(article_id: str) -> Response:
    """Returns the user's like status for the article."""
    # Get the user's like status for the article with the given ID
    like_status = (
        db.session.execute(
            db.select(LikeTable).filter_by(
                UserID=current_user.id,
                ArticleID=article_id,
            ),
        ).scalar()
        is not None
    )
    return jsonify({"like_status": like_status})


@app.route("/api/get_article_bookmark_status/<string:article_id>", methods=["GET"])
@login_required
def get_article_bookmark_status(article_id: str) -> Response:
    """Returns the user's bookmark status for the article."""
    # Get the user's bookmark status for the article with the given ID
    bookmark_status = (
        db.session.execute(
            db.select(Bookmark).filter_by(
                UserID=current_user.id,
                ArticleID=article_id,
            ),
        ).scalar()
        is not None
    )
    return jsonify({"bookmark_status": bookmark_status})


@app.route("/api/like_article/<string:article_id>", methods=["GET", "POST"])
@login_required
def like_article(article_id: str) -> Response:
    """Likes the article."""
    try:
        # Like the article with the given ID
        new_like = LikeTable(current_user.id, article_id)
        db.session.add(new_like)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not like article."})
    return jsonify({"success": "Successfully liked article."})


@app.route("/api/unlike_article/<string:article_id>", methods=["GET"])
@login_required
def unlike_article(article_id: str) -> Response:
    """Unlikes the article."""
    try:
        # Unlike the article with the given ID
        db.session.execute(
            db.delete(LikeTable).filter(
                LikeTable.UserID == current_user.id,
                LikeTable.ArticleID == article_id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not unlike article."})
    return jsonify({"success": "Successfully unliked article."})


# ----------------- Company routes -----------------


@app.route("/api/get_companies", methods=["GET"])
def load_companies() -> Response:
    """Load all companies for display. Will replace main function with this soon."""
    companies = db.session.execute(db.select(Company)).scalars().all()
    return jsonify([company.to_dict() for company in companies])


@app.route("/api/get_company/<string:company_id>", methods=["GET"])
def get_company(company_id: str) -> Response:
    """Returns the company."""
    # Get the company with the given ID
    company = (
        db.session.execute(db.select(Company).filter_by(CompanyID=company_id))
        .scalars()
        .first()
    )
    if company is not None:
        return jsonify(company.to_dict())
    return jsonify({"error": "Company not found."})


@app.route("/api/get_company_follow_status/<string:company_id>", methods=["GET"])
@login_required
def get_company_follow_status(company_id: str) -> Response:
    """Returns the user's follow status for the company."""
    # Get the user's follow status for the company with the given ID
    follow_status = db.session.execute(
        db.select(Follow).filter_by(UserID=current_user.id, CompanyID=company_id),
    ).scalar()
    return jsonify({"follow_status": bool(follow_status)})


@app.route("/api/follow_company/<string:company_id>", methods=["GET", "POST"])
@login_required
def follow_company(company_id: str) -> Response:
    """Follows the company."""
    try:
        # Follow the company with the given ID
        new_follow = Follow(current_user.id, company_id)
        db.session.add(new_follow)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not follow company."})
    return jsonify({"success": "Successfully followed company."})


@app.route("/api/unfollow_company/<string:company_id>", methods=["GET"])
@login_required
def unfollow_company(company_id: str) -> Response:
    """Unfollows the company."""
    try:
        # Unfollow the company with the given ID
        db.session.execute(
            db.delete(Follow).filter(
                Follow.UserID == current_user.id,
                Follow.CompanyID == company_id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not unfollow company."})
    return jsonify({"success": "Successfully unfollowed company."})


@app.route("/api/get_company_articles/<string:company_id>", methods=["GET"])
def get_company_articles(company_id: str) -> Response:
    """Returns the company's articles."""
    # Get the company's articles with the given company ID
    articles = (
        db.session.execute(
            db.select(Article)
            .filter_by(CompanyID=company_id)
            .order_by(desc(Article.PublicationDate))
            .limit(3),
        )
        .scalars()
        .all()
    )
    articles_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "date": article.PublicationDate,
            "summary": article.Summary,
            "score": article.PredictionScore,
        }
        for article in articles
    ]
    return jsonify(articles_list)


# ----------------- FAQ routes -----------------


@app.route("/api/get_questions", methods=["GET"])
def get_questions() -> Response:
    """Returns the support page."""
    questions = db.session.execute(db.select(Faq)).scalars().all()
    questions_list = [
        {
            "id": question.FAQID,
            "question": question.Question,
            "answer": question.Answer,
        }
        for question in questions
    ]
    return jsonify(questions_list)


@app.route("/api/submit_question", methods=["GET", "POST"])
@login_required
def submit_question() -> Response:
    """Submits a support question."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    question = request.json["question"]
    if len(question) < MIN_COMMENT_LENGTH or len(question) > MAX_COMMENT_LENGTH:
        return jsonify({"error": "Question must be between 1 and 10000 characters."})
    try:
        # Add a question to the support page
        new_question = UserQuestion(current_user.id, question)
        db.session.add(new_question)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not submit question."})
    return jsonify(
        {"success": "Question submitted. We will respond as soon as possible."},
    )


# ----------------- Notification routes -----------------


@app.route("/api/get_notifications", methods=["GET"])
@login_required
def get_notifications() -> Response:
    """Returns the user's notifications."""
    # Mark all notifications as read
    unread_notifications = UserNotificationRead.query.filter_by(
        UserID=current_user.id,
        IsRead=0,
    ).all()
    for notification in unread_notifications:
        notification.IsRead = 1
    db.session.commit()
    # Get the user's notifications by newest first
    user_notifications = (
        db.session.execute(
            db.select(UserNotificationRead)
            .join(
                Notification,
                UserNotificationRead.NotificationID == Notification.NotificationID,
            )
            .filter(UserNotificationRead.UserID == current_user.id)
            .order_by(desc(Notification.Time)),
        )
        .scalars()
        .all()
    )
    notification_data = [
        {
            "id": user_notification.UserNotificationReadID,
            "article_id": db.session.execute(
                db.select(Notification.ArticleID).filter_by(
                    NotificationID=user_notification.NotificationID,
                ),
            ).scalar(),
            "content": db.session.execute(
                db.select(Notification.Content).filter_by(
                    NotificationID=user_notification.NotificationID,
                ),
            ).scalar(),
            "time": db.session.execute(
                db.select(Notification.Time).filter_by(
                    NotificationID=user_notification.NotificationID,
                ),
            ).scalar(),
        }
        for user_notification in user_notifications
    ]
    return jsonify(notification_data)


@app.route("/api/get_notification_count", methods=["GET"])
@login_required
def get_notification_count() -> Response:
    """Returns the user's unread notification count."""
    # Get the user's unread notification count
    notif_count = db.session.execute(
        db.select(db.func.count())
        .select_from(UserNotificationRead)
        .filter_by(
            UserID=current_user.id,
            IsRead=0,
        ),
    ).scalar()
    return jsonify({"count": notif_count})


@app.route("/api/delete_notification/<string:notification_id>", methods=["GET"])
@login_required
def delete_notification(notification_id: str) -> Response:
    """Deletes the user's notification."""
    try:
        # Delete the user's notification with the given ID
        db.session.execute(
            db.delete(UserNotificationRead).filter(
                UserNotificationRead.UserNotificationReadID == notification_id,
                UserNotificationRead.UserID == current_user.id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not delete notification."})
    return jsonify({"success": "Successfully deleted notification."})


@scheduler.task("cron", id="add_daily_notif", hour=8, minute=0)
def add_daily_notif() -> None:
    """Adds a daily notification for the user."""
    with scheduler.app.app_context():
        new_notif = Notification(
            None,
            "The company details have been updated. Check it out!",
        )
        db.session.add(new_notif)
        db.session.commit()
        users = db.session.execute(db.select(User)).scalars().all()
        for user in users:
            new_user_notif = UserNotificationRead(user.id, new_notif.NotificationID)
            db.session.add(new_user_notif)
            db.session.commit()


# ----------------- Bookmark routes -----------------


@app.route("/api/get_bookmarks", methods=["GET"])
@login_required
def get_bookmarks() -> Response:
    """Returns the user's bookmarks."""
    # Get the user's bookmarks
    bookmarks = (
        db.session.execute(
            db.select(Bookmark)
            .join(Article, Bookmark.ArticleID == Article.ArticleID)
            .filter(Bookmark.UserID == current_user.id)
            .order_by(desc(Bookmark.BookmarkDate)),
        )
        .scalars()
        .all()
    )
    bookmarks_list = [
        {
            "id": bookmark.BookmarkID,
            "article_id": bookmark.ArticleID,
            "title": db.session.execute(
                db.select(Article.Title).filter_by(
                    ArticleID=bookmark.ArticleID,
                ),
            ).scalar(),
            "date": bookmark.BookmarkDate,
            "summary": db.session.execute(
                db.select(Article.Summary).filter_by(
                    ArticleID=bookmark.ArticleID,
                ),
            ).scalar(),
        }
        for bookmark in bookmarks
    ]
    return jsonify(bookmarks_list)


@app.route("/api/add_bookmark/<string:article_id>", methods=["GET", "POST"])
@login_required
def add_bookmark(article_id: str) -> Response:
    """Adds a bookmark for the user."""
    try:
        # Add a bookmark for the user with the given article ID
        new_bookmark = Bookmark(current_user.id, article_id)
        db.session.add(new_bookmark)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not add bookmark."})
    return jsonify({"success": "Successfully added bookmark."})


@app.route("/api/delete_bookmark/<string:article_id>", methods=["GET"])
@login_required
def delete_bookmark(article_id: str) -> Response:
    """Deletes the user's bookmark."""
    try:
        # Delete the user's bookmark with the given article ID
        db.session.execute(
            db.delete(Bookmark).filter(
                Bookmark.ArticleID == article_id,
                Bookmark.UserID == current_user.id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not delete bookmark."})
    return jsonify({"success": "Successfully deleted bookmark."})


# ----------------- Profile routes -----------------


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile() -> Response:
    """Returns the user's profile."""
    return redirect("http://localhost:3000/profile", code=301)


@app.route("/api/get_profile_data", methods=["GET"])
@login_required
def get_profile_data() -> Response:
    """Returns the user's profile data."""
    user = {
        "username": current_user.Username,
        "email": current_user.Email,
        "is_verified": current_user.IsVerified,
    }
    return jsonify(user)


@app.route("/api/verify_email", methods=["GET"])
@login_required
def verify_email() -> Response:
    """Sends a verification email to the user."""
    return send_verify_email(current_user)


@app.route("/api/logout")
@login_required
def logout() -> Response:
    """Logs out the user."""
    session.clear()
    logout_user()
    return jsonify({"success": "Successfully logged out."})


@app.route("/api/delete_user", methods=["GET"])
@login_required
def delete_user() -> Response:
    """Deletes the user."""
    user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar()
    session.clear()
    logout_user()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home", success="Successfully deleted account."), code=301)


if __name__ == "__main__":
    app.run(debug=os.environ["ENV"] == "dev", port=8080)
