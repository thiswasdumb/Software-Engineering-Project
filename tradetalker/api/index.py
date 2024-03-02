"""Contains the Flask application to send data to the TradeTalker frontend."""

import os
import re
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
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from werkzeug.wrappers import Response

from database.database_connection import DataBaseConnection
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
    add_data,
    db,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb:///tradetalkerdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
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


reset = True
if reset:
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_data()


sql_db = DataBaseConnection("localhost", "root", "", "tradetalkerdb")

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
    """Redirects to the TradeTalker frontend."""
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
            db.session.commit()  # Commit the transaction
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


@app.route("/api/forgot_password", methods=["GET"])
def forgot_password() -> Response:
    """Returns the forgot password page."""
    return redirect("http://localhost:3000/forgot_password", code=301)


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
    companies = (
        db.session.execute(
            db.select(Company).filter(Company.CompanyName.like(f"%{query}%")),
        )
        .scalars()
        .all()
    )
    articles_list = [
        {
            "id": article.ArticleID,
            "title": article.Title,
            "summary": article.Summary,
        }
        for article in articles
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
    return jsonify({"articles": articles_list, "companies": companies_list})


# ----------------- Dashboard routes -----------------


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
def get_dashboard_data() -> Response:
    """Returns the user's dashboard data."""
    if current_user.is_authenticated:  # Currently buggy with @login_required
        return jsonify({"username": current_user.Username})
    return jsonify({"error": "You are not logged in."})


@app.route("/api/get_followed_companies", methods=["GET"])
@login_required
def get_followed_companies() -> Response:
    """Returns the user's followed companies."""
    followed_companies = (
        db.session.execute(
            db.select(Follow)
            .join(Company, Follow.CompanyID == Company.CompanyID)
            .filter(Follow.UserID == current_user.id)
            .add_columns(Company.CompanyName),
        )
        .scalars()
        .all()
    )
    followed_companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
        }
        for company in followed_companies
    ]
    return jsonify(followed_companies_list)


# ----------------- Stocks routes -----------------


@app.route("/api/get_stock_trends", methods=["GET"])
def get_stock_trends() -> Response:
    """Returns the stock trends."""
    # Get the stock trends
    stock_trends = (
        db.session.execute(db.select(Company).order_by(Company.StockVariance.desc()))
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


@app.route("/api/get_leaderboard", methods=["GET"])
def get_leaderboard() -> Response:
    """Returns the leaderboard."""
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
    # Get the company name of the article using the company ID
    company_name = (
        db.session.execute(
            db.select(Company.CompanyName).filter_by(CompanyID=article.CompanyID),
        )
        .scalars()
        .first()
    )
    if article is not None:
        article_json = {
            "company_name": company_name,
            "company_id": article.CompanyID,
            "title": article.Title,
            "content": article.Content,
            "publication_date": article.PublicationDate,
            "url": article.URL,
            "source": article.Source,
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


@app.route("/api/add_article_comment/<string:article_id>", methods=["POST"])
@login_required
def add_article_comment(article_id: str) -> Response:
    """Adds a comment to the article."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    comment = request.json["content"]
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


@app.route(
    "/api/add_article_reply/<string:article_id>/<string:comment_id>",
    methods=["POST"],
)
@login_required
def add_article_reply(article_id: str, comment_id: str) -> Response:
    """Adds a reply to the article comment."""
    if request.json is None:
        return jsonify({"error": "Invalid request."})
    reply = request.json["content"]
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
    like_status = db.session.execute(
        db.select(LikeTable).filter_by(UserID=current_user.id, ArticleID=article_id),
    ).scalar()
    return jsonify({"like_status": bool(like_status)})


@app.route("/api/get_article_bookmark_status/<string:article_id>", methods=["GET"])
@login_required
def get_article_bookmark_status(article_id: str) -> Response:
    """Returns the user's bookmark status for the article."""
    # Get the user's bookmark status for the article with the given ID
    bookmark_status = db.session.execute(
        db.select(Bookmark).filter_by(UserID=current_user.id, ArticleID=article_id),
    ).scalar()
    return jsonify({"bookmark_status": bool(bookmark_status)})


@app.route("/api/like_article/<string:article_id>", methods=["POST"])
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


@app.route("/api/unlike_article/<string:article_id>", methods=["DELETE"])
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


@app.route("/api/bookmark_article/<string:article_id>", methods=["POST"])
@login_required
def bookmark_article(article_id: str) -> Response:
    """Bookmarks the article."""
    try:
        # Bookmark the article with the given ID
        new_bookmark = Bookmark(current_user.id, article_id)
        db.session.add(new_bookmark)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not bookmark article."})
    return jsonify({"success": "Successfully bookmarked article."})


@app.route("/api/unbookmark_article/<string:article_id>", methods=["DELETE"])
@login_required
def unbookmark_article(article_id: str) -> Response:
    """Unbookmarks the article."""
    try:
        # Unbookmark the article with the given ID
        db.session.execute(
            db.delete(Bookmark).filter(
                Bookmark.UserID == current_user.id,
                Bookmark.ArticleID == article_id,
            ),
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Could not unbookmark article."})
    return jsonify({"success": "Successfully unbookmarked article."})


# ----------------- Company routes -----------------


@app.route("/api/get_companies", methods=["GET"])
def get_companies() -> Response:
    """Returns the companies."""
    # Select all companies
    companies = db.session.execute(db.select(Company)).scalars().all()
    companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "stock_price": company.StockPrice,
            "symbol": company.StockSymbol,
            "industry": company.Industry,
            "description": company.CompanyDescription,
            "predicted_stock_price": company.PredictedStockPrice,
            "stock_variance": company.StockVariance,
        }
        for company in companies
    ]
    return jsonify(companies_list)


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
        company_json = {
            "company_name": company.CompanyName,
            "stock_symbol": company.StockSymbol,
            "stock_price": company.StockPrice,
            "industry": company.Industry,
            "description": company.CompanyDescription,
            "predicted_stock_price": company.PredictedStockPrice,
            "stock_variance": company.StockVariance,
        }
        return jsonify(company_json)
    return jsonify({"error": "Company not found."})


@app.route("/api/follow_company/<string:company_id>", methods=["POST"])
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
    notifications = (
        db.session.execute(
            db.select(Notification)
            .join(UserNotificationRead)
            .filter(UserNotificationRead.UserID == current_user.id)
            .order_by(desc(Notification.Time)),
        )
        .scalars()
        .all()
    )
    notification_data = [
        {
            "id": notification.NotificationID,
            "article_id": notification.ArticleID,
            "content": notification.Content,
            "time": notification.Time,
        }
        for notification in notifications
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
            .filter(Bookmark.UserID == current_user.id),
        )
        .scalars()
        .all()
    )
    bookmarks_list = [
        {
            "id": bookmark.ArticleID,
            "title": bookmark.Title,
            "summary": bookmark.Summary,
        }
        for bookmark in bookmarks
    ]
    return jsonify(bookmarks_list)


@app.route("/api/add_bookmark/<string:article_id>", methods=["POST"])
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


@app.route("/api/delete_bookmark/<string:article_id>", methods=["DELETE"])
@login_required
def delete_bookmark(article_id: str) -> Response:
    """Deletes the user's bookmark."""
    try:
        # Delete the user's bookmark with the given article ID
        db.session.execute(
            db.delete(Bookmark).where(
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
        "preferences": current_user.Preferences,
    }
    return jsonify(user)


@app.route("/api/logout")
@login_required
def logout() -> Response:
    """Logs out the user."""
    session.clear()
    logout_user()
    return jsonify({"success": "Successfully logged out."})


@app.route("/api/delete_user", methods=["GET"])
def delete_user() -> Response:
    """Deletes the user."""
    if current_user.is_authenticated:
        session.clear()  # Remove the sessions
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
