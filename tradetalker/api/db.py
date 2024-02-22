"""Database class to handle all the database queries."""

from datetime import datetime

from flask import Flask
from flask_mysqldb import MySQL


class Database:
    """Class to handle all the database queries."""

    def __init__(self, app: Flask) -> None:
        """Initializes the database connection."""
        self.mysql = MySQL()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initializes the database connection with the Flask app."""
        self.mysql.init_app(app)

    def insert_user(
        self,
        username: str,
        password: str,
        email: str,
        preferences: int,
    ) -> None:
        """Inserts a new user into the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                """INSERT INTO User (Username, Password, Email, Preferences)
                VALUES (%s, %s, %s, %s)""",
                (username, password, email, preferences),
            )
            self.mysql.connect.commit()

    def select_all_users(self) -> list:
        """Selects all users from the database."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()

    # ---------------- Article table methods ---------------- #
    def insert_article(
        self,
        title: str,
        content: str,
        publication_date: datetime,
        url: str,
        summary: str,
    ) -> None:
        """Inserts a new article into the database.

        Note for empty fields (CompanyID, PredictionScore):
        The table has 1 primary key which is the ID (not available in the article text or title
        itself). Therefore, it's more efficient to have these values inserted in the initial
        insertion as finding the article at a later stage based on metrics such as title might
        be subject to fault and have a significant computational cost.
        To be discussed.
        """
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Article (Title, Content, PublicationDate, URL, Summary)
                VALUES (%s, %s, %s, %s, %s)""",
                (title, content, publication_date, url, summary),
            )
            self.mysql.connect.commit()

    # ----------------  Company table methods ---------------- #

    def insert_company(
        self,
        company_name: str,
        stock_symbol: str,
        stock_price: int,
        industry: str,
        company_description: str,
    ) -> None:
        """Inserts a new company into the database.

        For initial insertion.
        """
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Company (CompanyName, StockSymbol, StockPrice, Industry, CompanyDescription)
                VALUES (%s, %s, %f, %s, %s)""",
                (
                    company_name,
                    stock_symbol,
                    stock_price,
                    industry,
                    company_description,
                ),
            )
            self.mysql.connect.commit()

    def update_company_predicted_stock_price(
        self,
        company_name: str,
        predicted_stock_price: int,
    ) -> None:
        """Updates the predicted stock price of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET PredictedStockPrice = %f WHERE CompanyName = %s",
                (predicted_stock_price, company_name),
            )
            self.mysql.connect.commit()

    def update_company_stock_variance(
        self,
        company_name: str,
        stock_variance: int,
    ) -> None:
        """Updates the stock variance of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET StockVariance = %f WHERE CompanyName = %s",
                (stock_variance, company_name),
            )
            self.mysql.connect.commit()

    def update_company_sentiment_score(
        self,
        company_name: str,
        sentiment_score: int,
    ) -> None:
        """Updates the sentiment score of a company."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "UPDATE Company SET SentimentScore = %f WHERE CompanyName = %s",
                (sentiment_score, company_name),
            )
        self.mysql.connect.commit()

    # Note for the 3 functions above:
    # If we can update the 3 fields at the same time using the API, we can reduce the costs heavily
    # -----To be discussed

    # ----------------  Like table methods ---------------- #
    def like_relation_exists(self, user_id: int, article_id: int) -> bool:
        """Checks if a user has liked an article already."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM LikeTable Where UserID = %d AND ArticleID = %d",
                (user_id, article_id),
            )
            result = cursor.fetchone()
            return result is not None

    def toggle_like(self, user_id: int, article_id: int) -> bool:
        """Toggles the like status of an article.

        If the relation exists, it means the user is unliking and we remove the relation.
        If not, the user is liking and we create.
        """
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
        # Returning the result for further functionalities
        return like_exists

    # ----------------  Bookmark table methods ---------------- #
    def bookmark_relation_exists(self, user_id: int, article_id: int) -> bool:
        """Checks if a user has bookmarked an article already."""
        with self.mysql.connect.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Bookmark Where UserID = %d AND ArticleID = %d",
                (user_id, article_id),
            )
            result = cursor.fetchone()
            return result is not None

    def bookmark_like(self, user_id: int, article_id: int) -> bool:
        """Toggles the bookmark status of an article.

        If the relation exists, it means the user is unbookmarking and we remove the relation.
        If not, the user is bookmarking and we create.
        """
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
