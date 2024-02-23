"""Database class to handle all the database queries."""

from datetime import datetime

from flask import Flask
from flask_mysqldb import MySQL


class Database:
    """Class to handle all the database queries."""

    def __init__(self, app: Flask | None) -> None:
        """Initializes the database connection."""
        self.mysql = MySQL()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initializes the database connection for Flask use."""
        self.mysql.init_app(app)

    def user_insert(
        self,
        username: str,
        password: str,
        email: str,
        preferences: int,
    ) -> None:
        """Inserts a new user into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO User (Username, Password, Email, Preferences) VALUES (%s, %s, %s, %s)",
                (username, password, email, preferences),
            )
            self.mysql.connect.commit()

    def user_select_all(self) -> list:
        """Selects all users from the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()

    # -----------------------------------  Article table methods ----------------------------------- #
    def article_insert_article(
        self,
        title: str,
        content: str,
        publication_date: datetime,
        url: str,
        summary: str,
    ) -> None:
        """Inserts a new article into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Article (Title, Content, PublicationDate, URL, Summary) VALUES "
                "(%s, %s, %s, %s, %s)",
                (title, content, publication_date, url, summary),
            )
            self.mysql.connect.commit()

            # note for empty fields (CompanyID, PredictionScore)
            # The table has 1 primary key which is the ID (not available in the article text or title itself)
            # therefor it's more efficient to have these values inserted in the initial insertion
            # as finding the article at a later stage based on metrics such as title might be subject to fault and
            # have a significant computational cost ----- To be discussed

    # -----------------------------------  Company table methods ----------------------------------- #
    # for initial insertion
    def company_insert_company(
        self,
        company_name: str,
        stock_symbol: str,
        stock_price: float,
        industry: str,
        company_description: str,
    ) -> None:
        """Inserts a new company into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Company (CompanyName, StockSymbol, StockPrice, Industry, CompanyDescription) VALUES "
                "(%s, %s, %f, %s, %s)",
                (
                    company_name,
                    stock_symbol,
                    stock_price,
                    industry,
                    company_description,
                ),
            )
            self.mysql.connect.commit()

    def company_update_stock_price(self, company_name: str, stock_price: float) -> None:
        """Updates the stock price of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET StockPrice = %f WHERE CompanyName = %s",
                (stock_price, company_name),
            )
            self.mysql.connect.commit()

    # update PredictedStockPrice
    def company_update_predicted_stock_price(
        self,
        company_name: str,
        predicted_stock_price: float,
    ) -> None:
        """Updates the predicted stock price of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET PredictedStockPrice = %f WHERE CompanyName = %s",
                (predicted_stock_price, company_name),
            )
            self.mysql.connect.commit()

    # update StockVariance
    def company_update_stock_variance(
        self,
        company_name: str,
        stock_variance: float,
    ) -> None:
        """Updates the stock variance of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET StockVariance = %f WHERE CompanyName = %s",
                (stock_variance, company_name),
            )
            self.mysql.connect.commit()

    # update SentimentScore
    def company_update_sentiment_score(
        self,
        company_name: str,
        sentiment_score: float,
    ) -> None:
        """Updates the sentiment score of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET SentimentScore = %f WHERE CompanyName = %s",
                (sentiment_score, company_name),
            )
        self.mysql.connect.commit()

    # note for the 3 functions above:
    # if we can update the 3 fields at the same time using the API, we can reduce the costs heavily -----To be discussed

    # This function is used for the company message
    def company_select_all(self) -> list:
        """Selects all companies from the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM Company")
            return cursor.fetchall()

    # This function can be used for the company pop-up box
    def company_select_by_name(self, company_name: str) -> dict:
        """Selects a company by its name."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Company WHERE CompanyName = %s",
                (company_name,),
            )
            return cursor.fetchone()

    # This function will be used for categorizing companies and for the recommendation system
    def company_select_by_industry(self, industry: str) -> list:
        """Selects companies by their industry."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM Company WHERE Industry = %s", (industry,))
            return cursor.fetchall()

    # -----------------------------------  Follow table methods ----------------------------------- #
    # Function to see if a user follows a company or not
    def follow_check(self, user_id: int, company_id: int) -> dict:
        """Checks if a user follows a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Follow WHERE UserID = %d AND CompanyID = %d",
                (user_id, company_id),
            )
            return cursor.fetchone()

    # A toggle function for the follow button, if following already, unfollow and vice-versa
    def follow_toggle(
        self,
        user_id: int,
        company_id: int,
        follow_date: datetime,
    ) -> dict:
        """Toggles the follow status of a user for a company."""
        is_following = self.follow_check(user_id, company_id)
        with self.mysql.connect.cursor() as cursor:
            if is_following:
                cursor.execute(
                    "DELETE FROM Follow WHERE UserID = %d AND CompanyID = %d",
                    (user_id, company_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO Follow (UserID, CompanyID, FollowDate) VALUES (%d, %d, %d)",
                    (user_id, company_id, follow_date),
                )
            self.mysql.connect.commit()
        # returning the previous state as well -- can be current, if needed for simplicity
        return is_following

    # Function that returns company_id of all the companies that a user is following
    def follow_get_user_following_companies(self, user_id: int) -> list:
        """Returns the company IDs of all the companies that a user is following."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT CompanyID FROM Follow WHERE UserID = % d",
                (user_id,),
            )
            return cursor.fetchall()

    # -----------------------------------  Like table methods ----------------------------------- #
    # function to see if a user has liked an article already
    def like_relation_exists(self, user_id: int, article_id: int) -> bool:
        """Checks if a user has liked an article already."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM LikeTable Where UserID = %d AND ArticleID = %d",
                (user_id, article_id),
            )
            return cursor.fetchone() is not None

    # function that is connected to the like button, if the relation exists, it means the user is unliking
    # and we remove the relation, if not, the user is liking and we create
    def toggle_like(self, user_id: int, article_id: int) -> bool:
        """Toggles the like status of an article."""
        like_exists = self.like_relation_exists(user_id, article_id)
        with self.mysql.connect.cursor() as cursor:
            if like_exists:
                cursor.execute(
                    "DELETE FROM LikeTable WHERE UserID = %d AND ArticleID = %d",
                    (user_id, article_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO LikeTable (UserID, ArticleID) VALUES (%d, %d)",
                    (user_id, article_id),
                )
            self.mysql.connect.commit()
        # returning the result for further functionalities
        return like_exists

    # -----------------------------------  Bookmark table methods ----------------------------------- #
    # function to see if a user has bookmarked an article already
    def bookmark_relation_exists(self, user_id: int, article_id: int) -> bool:
        """Checks if a user has bookmarked an article already."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Bookmark Where UserID = %d AND ArticleID = %d",
                (user_id, article_id),
            )
            result = cursor.fetchone()
            return result is not None

    # function that is connected to the bookmark button, if the relation exists, it means the user is unbookmarking
    # and we remove the relation, if not, the user is bookmarking and we create
    def toggle_bookmark(self, user_id: int, article_id: int) -> bool:
        """Toggles the bookmark status of an article."""
        bookmark_exists = self.bookmark_relation_exists(user_id, article_id)
        with self.mysql.connect.cursor() as cursor:
            if bookmark_exists:
                cursor.execute(
                    "DELETE FROM Bookmark WHERE UserID = %d AND ArticleID = %d",
                    (user_id, article_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO Bookmark (UserID, ArticleID) VALUES (%d, %d)",
                    (user_id, article_id),
                )
            self.mysql.connect.commit()
        # returning the result for further functionalities
        return bookmark_exists

    # -----------------------------------  FAQ table methods ----------------------------------- #
    # Basic selection, faq insertions will be done manually
    def faq_select_all(self) -> list:
        """Selects all FAQs from the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM FAQ")
            return cursor.fetchall()

    # -----------------------------------  UserQuestion table methods ----------------------------------- #
    # Basic insertion
    def user_question_insert(self, user_id: int, question: str, time: int) -> None:
        """Inserts a new user question into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO UserQuestion (UserID, Question, Time) VALUES (%d, %s, %d)",
                (user_id, question, time),
            )
            self.mysql.connect.commit()

    # When we answer the user question we mark it as answered
    def user_question_mark_answered(self, user_question_id: int) -> None:
        """Marks a user question as answered."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE UserQuestion SET IsAnswered = 1 WHERE UserQuestionID = %d",
                (user_question_id,),
            )
            self.mysql.connect.commit()

    # -----------------------------------  ArticleComment table methods ----------------------------------- #
    # Basic insertion, based on the availability of the parent_comment_id
    def article_comment_insert(
        self,
        user_id: int,
        article_id: int,
        content: str,
        time: int,
        parent_comment_id: int | None,
    ) -> None:
        """Inserts a new comment for an article into the database."""
        with self.mysql.connect.cursor() as cursor:
            if parent_comment_id:
                cursor.execute(
                    "INSERT INTO ArticleComment (UserID, ArticleID, Content, Time, ParentCommentID) "
                    "VALUES (%d, %d, %s, %d, %d)",
                    (user_id, article_id, content, time, parent_comment_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO ArticleComment (UserID, ArticleID, Content, Time) "
                    "VALUES (%d, %d, %s, %d, %d)",
                    (user_id, article_id, content, time),
                )
            self.mysql.connect.commit()

    # Function to select all comments for an article, to be displayed below the article
    def article_comment_select_by_article(self, article_id: int) -> list:
        """Selects all comments for an article."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM ArticleComment WHERE ArticleID = %d",
                (article_id,),
            )
            return cursor.fetchall()

    # -----------------------------------  Notification table methods ----------------------------------- #
    # Basic insertion into the Notification table
    def notification_insert(self, article_id: int, content: str, time: int) -> None:
        """Inserts a new notification into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Notification (ArticleID, Content, Time) VALUES (%d, %s, %d)",
                (article_id, content, time),
            )
            self.mysql.connect.commit()

    # -----------------------------------  UserNotificationRead table methods ----------------------------------- #
    # Basic insertion into the UserNotificationRead table
    def user_notification_read_insert(self, user_id: int, notification_id: int) -> None:
        """Inserts a new notification as read for a user."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "INSERT INTO UserNotificationRead (UserID, NotificationID) VALUES (%d, %d)",
                (user_id, notification_id),
            )
            self.mysql.connect.commit()

    # Function to fetch all notifications of a user
    def user_notification_read_select_all_notifications(self, user_id: int) -> list:
        """Selects all notifications of a user."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM UserNotificationRead WHERE UserID = %d",
                (user_id,),
            )
            return cursor.fetchall()

    # Function to mark a notification as read for a user
    def user_notification_read_mark_read(self, user_notification_read_id: int) -> None:
        """Marks a notification as read for a user."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE UserNotificationRead SET IsRead = 1 WHERE UserNotificationID = %d",
                (user_notification_read_id,),
            )
            self.mysql.connect.commit()

    # Function to fetch all unread notifications of a user
    def user_notification_read_select_unread(self, user_id: int) -> list:
        """Selects all unread notifications of a user."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM UserNotificationRead WHERE UserID = %d AND IsRead = 0",
                (user_id,),
            )
            return cursor.fetchall()
