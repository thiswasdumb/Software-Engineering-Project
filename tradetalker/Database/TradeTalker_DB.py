from flask_mysqldb import MySQL


class Database:
    def __init__(self, app=None):
        self.mysql = MySQL()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.mysql.init_app(app)

    def insert_user(self, username, password, email, preferences):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO User (Username, Password, Email, Preferences) VALUES (%s, %s, %s, %s)", (username, password, email, preferences))
            self.mysql.connection.commit()

    def select_all_users(self):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()

    # -----------------------------------  Article table methods ----------------------------------- #
    def insert_article(self, title, content, publication_date, url, summary):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Article (Title, Content, PublicationDate, URL, Summary) VALUES (%s, %s, %s, %s, %s)",
                           (title, content, publication_date, url, summary))
            self.mysql.connection.commit()

            # note for empty fields (CompanyID, PredictionScore)
            # The table has 1 primary key which is the ID (not available in the article text or title itself)
            # therefor it's more efficient to have these values inserted in the initial insertion
            # as finding the article at a later stage based on metrics such as title might be subject to fault and
            # have a significant computational cost ----- To be discussed

    # -----------------------------------  Company table methods ----------------------------------- #
    # for initial insertion
    def insert_company(self, company_name, stock_symbol, stock_price, industry, company_description):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Company (CompanyName, StockSymbol, StockPrice, Industry, CompanyDescription) VALUES (%s, %s, %f, %s, %s)",
                           (company_name, stock_symbol, stock_price, industry, company_description))
            self.mysql.connection.commit()

    # update PredictedStockPrice
    def update_company_predicted_stock_price(self, company_name, predicted_stock_price):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET PredictedStockPrice = %f WHERE CompanyName = %s", (predicted_stock_price,
                                                                                                  company_name))
            self.mysql.connection.commit()

    # update StockVariance
    def update_company_stock_variance(self, company_name, stock_variance):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET StockVariance = %f WHERE CompanyName = %s", (stock_variance,
                                                                                            company_name))
            self.mysql.connection.commit()

    # update SentimentScore
    def update_company_sentiment_score(self, company_name, sentiment_score):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET SentimentScore = %f WHERE CompanyName = %s", (sentiment_score,
                                                                                             company_name))
        self.mysql.connection.commit()

    # note for the 3 functions above:
    # if we can update the 3 fields at the same time using the API, we can reduce the costs heavily -----To be discussed

    # -----------------------------------  Like table methods ----------------------------------- #
    # function to see if a user has liked an article already
    def like_relation_exists(self, user_id, article_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM LikeTable Where UserID = %d AND ArticleID = %d", (user_id, article_id))
            result = cursor.fetchone()
            return result is not None

    # function that is connected to the like button, if the relation exists, it means the user is unliking
    # and we remove the relation, if not, the user is liking and we create
    def toggle_like(self, user_id, article_id):
        like_exists = self.like_relation_exists(user_id, article_id)
        with self.mysql.connection.cursor() as cursor:
            if like_exists:
                cursor.execute(
                    "DELETE FROM LikeTable WHERE UserID = %d AND ArticleID = %d", (user_id, article_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO LikeTable (UserID, ArticleID) VALUES (%d, %d)", (user_id, article_id)
                )
            self.mysql.connection.commit()
        # returning the result for further functionalities
        return like_exists


    # -----------------------------------  Bookmark table methods ----------------------------------- #
    # function to see if a user has bookmarked an article already
    def bookmark_relation_exists(self, user_id, article_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Bookmark Where UserID = %d AND ArticleID = %d", (user_id, article_id))
            result = cursor.fetchone()
            return result is not None

    # function that is connected to the bookmark button, if the relation exists, it means the user is unbookmarking
    # and we remove the relation, if not, the user is bookmarking and we create
    def bookmark_like(self, user_id, article_id):
        bookmark_exists = self.bookmark_relation_exists(user_id, article_id)
        with self.mysql.connection.cursor() as cursor:
            if bookmark_exists:
                cursor.execute(
                    "DELETE FROM Bookmark WHERE UserID = %d AND ArticleID = %d", (user_id, article_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO Bookmark (UserID, ArticleID) VALUES (%d, %d)", (user_id, article_id)
                )
            self.mysql.connection.commit()
        # returning the result for further functionalities
        return bookmark_exists
