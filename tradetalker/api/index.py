"""Contains the Flask application to send data to the TradeTalker frontend."""
import datetime
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
    update_all_companies_daily,
    get_company_article_sentiment_scores,
    get_all_company_names,
    get_articles_by_company_name,
    get_article_from_news_script,
    get_company_data_for_linear_regression,
)

from linear_regression import Linear_Regression

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


reset = True  # Set to False to keep the database data on restart
if reset:
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_base_company_data()
        add_data()
        get_company_article_sentiment_scores(1)
        get_all_company_names()
        get_article_from_news_script({
            'Company': "3i",
            'Title': "Test article for 3i",
            'Content': "Blah blah blah 3i so good",
            'URL': "idk.whocares",
            'Summary': "3i nice!",
            'PublicationDate': datetime.datetime.now(),
            'ProcessedArticle': "Article processed!",
            "PredictionScore": 1
        })
        print(get_articles_by_company_name("3i"))
        company_name="3i"
        comp = db.session.execute(db.select(Company).filter(Company.CompanyName.like(f'%{company_name}%'))
                                     ).scalars().first()
        print(comp)
        comp_data = get_company_data_for_linear_regression(comp)
        print(comp_data)
        predicted_price = Linear_Regression.Linear_Regression(
            comp_data['StockSymbol'], comp_data['SentimentScores'], comp_data['PriceHistoric']
        ).calculate_stock_price()
        print(predicted_price)




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
    """Returns the user's recommended articles."""
    return jsonify({"error": "Not implemented yet."})


@app.route("/api/get_recommended_companies", methods=["GET"])
@login_required
def get_recommended_companies() -> Response:
    """Returns the user's recommended companies."""
    # Right now this only selects 3 random companies that the user is not following
    followed_companies = (
        db.session.execute(
            db.select(Follow.CompanyID).filter(Follow.UserID == current_user.id),
        )
        .scalars()
        .all()
    )
    followed_company_ids = list(followed_companies)
    recommended_companies = (
        db.session.execute(
            db.select(Company)
            .filter(~Company.CompanyID.in_(followed_company_ids))
            .order_by(db.func.rand())
            .limit(3),
        )
        .scalars()
        .all()
    )
    recommended_companies_list = [
        {
            "id": company.CompanyID,
            "name": company.CompanyName,
            "symbol": company.StockSymbol,
        }
        for company in recommended_companies
    ]
    return jsonify(recommended_companies_list)


@app.route("/api/get_newsfeed", methods=["GET"])
@login_required
def get_newsfeed() -> Response:
    """Returns the 3 most recent articles from the followed companies."""
    # Get the 3 most recent articles from the followed companies
    newsfeed = (
        db.session.execute(
            db.select(Article)
            .join(Follow, Article.CompanyID == Follow.CompanyID)
            .filter(Follow.UserID == current_user.id)
            .order_by(desc(Article.PublicationDate))
            .limit(3),
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


@app.route("/api/check_verified", methods=["GET"])
@login_required
def check_verified() -> Response:
    """Returns whether the user is verified."""
    return jsonify({"verified": current_user.IsVerified})


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
    like_status = bool(
        db.session.execute(
            db.select(LikeTable).filter_by(
                UserID=current_user.id,
                ArticleID=article_id,
            ),
        ).scalar(),
    )
    return jsonify({"like_status": like_status})


@app.route("/api/get_article_bookmark_status/<string:article_id>", methods=["GET"])
@login_required
def get_article_bookmark_status(article_id: str) -> Response:
    """Returns the user's bookmark status for the article."""
    # Get the user's bookmark status for the article with the given ID
    bookmark_status = db.session.execute(
        db.select(Bookmark).filter_by(UserID=current_user.id, ArticleID=article_id),
    ).scalar()
    return jsonify({"bookmark_status": bool(bookmark_status)})


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


@app.route("/api/bookmark_article/<string:article_id>", methods=["GET", "POST"])
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


@app.route("/api/unbookmark_article/<string:article_id>", methods=["GET"])
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
@login_required
def delete_user() -> Response:
    """Deletes the user."""
    user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar()
    session.clear()
    logout_user()
    db.session.delete(user)
    db.session.commit()
    return redirect(
        url_for("home", success="Successfully deleted account!"),
        code=301,
    )


def daily_company_update() -> bool:
    """Calls once a day (?) to update price_related fields."""
    return update_all_companies_daily()

def predict_stock_price() -> None:
    companies = db.session.execute(db.select(Company)).scalars().all()
    for company in companies:
        # get the sentiment scores of the articles in the last 7 days
        article_sentiment_scores = []
        company_articles = db.session.execute(
            db.session(Article).filter_by(CompanyID=company.CompanyID)
        )


if __name__ == "__main__":
    app.run(debug=os.environ["ENV"] == "dev", port=8080)
