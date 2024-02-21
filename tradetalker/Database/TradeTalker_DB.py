from cgitb import reset
import re
from unittest import result
from flask_mysqldb import MySQL


class Database:
    def __init__(self, app=None):
        self.mysql = MySQL()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.mysql.init_app(app)

    def user_insert(self, username, password, email, preferences):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO User (Username, Password, Email, Preferences) VALUES (%s, %s, %s, %s)",
                           (username, password, email, preferences))
            self.mysql.connection.commit()

    def user_select_all(self):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()

    # -----------------------------------  Article table methods ----------------------------------- #
    def article_insert_article(self, title, content, publication_date, url, summary):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Article (Title, Content, PublicationDate, URL, Summary) VALUES "
                           "(%s, %s, %s, %s, %s)",
                           (title, content, publication_date, url, summary))
            self.mysql.connection.commit()

            # note for empty fields (CompanyID, PredictionScore)
            # The table has 1 primary key which is the ID (not available in the article text or title itself)
            # therefor it's more efficient to have these values inserted in the initial insertion
            # as finding the article at a later stage based on metrics such as title might be subject to fault and
            # have a significant computational cost ----- To be discussed

    # -----------------------------------  Company table methods ----------------------------------- #
    # for initial insertion
    def company_insert_company(self, company_name, stock_symbol, stock_price, industry, company_description):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Company (CompanyName, StockSymbol, StockPrice, Industry, CompanyDescription) VALUES "
                           "(%s, %s, %f, %s, %s)",
                           (company_name, stock_symbol, stock_price, industry, company_description))
            self.mysql.connection.commit()

    def company_update_stock_price(self, company_name, stock_price):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET StockPrice = %f WHERE CompanyName = %s", (stock_price, company_name))
            self.mysql.connection.commit()

    # update PredictedStockPrice
    def company_update_predicted_stock_price(self, company_name, predicted_stock_price):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET PredictedStockPrice = %f WHERE CompanyName = %s", (predicted_stock_price,
                                                                                                  company_name))
            self.mysql.connection.commit()

    # update StockVariance
    def company_update_stock_variance(self, company_name, stock_variance):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET StockVariance = %f WHERE CompanyName = %s", (stock_variance,
                                                                                            company_name))
            self.mysql.connection.commit()

    # update SentimentScore
    def company_update_sentiment_score(self, company_name, sentiment_score):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Company SET SentimentScore = %f WHERE CompanyName = %s", (sentiment_score,
                                                                                             company_name))
        self.mysql.connection.commit()

    # note for the 3 functions above:
    # if we can update the 3 fields at the same time using the API, we can reduce the costs heavily -----To be discussed

    # This function is used for the company message
    def company_select_all(self):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Company")
            result = cursor.fetchall()
            return result

    # This function can be used for the company pop-up box    
    def company_select_by_name(self, company_name):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Company WHERE CompanyName = %s", (company_name,))
            result = cursor.fetchone()
            return result

    # This function will be used for categorizing companies and for the recommendation system
    def company_select_by_industry(self, industry):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Company WHERE Industry = %s", (industry,))
            result = cursor.fetchall()
            return result

    # -----------------------------------  Follow table methods ----------------------------------- #
    # Function to see if a user follows a company or not
    def follow_check(self, user_id, company_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Follow WHERE UserID = %d AND CompanyID = %d", (user_id, company_id))
            result = cursor.fetchone()
            return result

    # A toggle function for the follow button, if following already, unfollow and vice-versa
    def follow_toggle(self, user_id, company_id, follow_date):
        is_following = self.follow_check(user_id, company_id)
        with self.mysql.connection.cursor() as cursor:
            if is_following:
                cursor.execute("DELETE FROM Follow WHERE UserID = %d AND CompanyID = %d", (user_id, company_id))
            else:
                cursor.execute("INSERT INTO Follow (UserID, CompanyID, FollowDate) VALUES (%d, %d, %d)",
                               (user_id, company_id, follow_date))
            self.mysql.connection.commit()
        # returning the previous state as well -- can be current, if needed for simplicity
        return is_following

    # Function that returns company_id of all the companies that a user is following
    def follow_get_user_following_companies(self, user_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT CompanyID FROM Follow WHERE UserID = % d", (user_id,))
            result = cursor.fetchall()
            return result

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
    def toggle_bookmark(self, user_id, article_id):
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

    # -----------------------------------  FAQ table methods ----------------------------------- #
    # Basic selection, faq insertions will be done manually
    def faq_select_all(self):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM FAQ")
            result = cursor.fetchall()
            return result

    # -----------------------------------  UserQuestion table methods ----------------------------------- #
    # Basic insertion
    def user_question_insert(self, user_id, question, time):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO UserQuestion (UserID, Question, Time) VALUES (%d, %s, %d)",
                                                                            (user_id, question, time))
            self.mysql.connection.commit()

    # When we answer the user question we mark it as answered
    def user_question_mark_answered(self, user_question_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE UserQuestion SET IsAnswered = 1 WHERE UserQuestionID = %d", (user_question_id,))
            self.mysql.connection.commit()

    # -----------------------------------  ArticleComment table methods ----------------------------------- #
    # Basic insertion, based on the availability of the parent_comment_id
    def article_comment_insert(self, user_id, article_id, content, time, parent_comment_id=None):
        with self.mysql.connection.cursor() as cursor:
            if parent_comment_id:
                cursor.execute("INSERT INTO ArticleComment (UserID, ArticleID, Content, Time, ParentCommentID) "
                               "VALUES (%d, %d, %s, %d, %d)", (user_id, article_id, content, time, parent_comment_id))
            else:
                cursor.execute("INSERT INTO ArticleComment (UserID, ArticleID, Content, Time) "
                               "VALUES (%d, %d, %s, %d, %d)", (user_id, article_id, content, time))
            self.mysql.connection.commit()

    # Function to select all comments for an article, to be displayed below the article
    def article_comment_select_by_article(self, article_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ArticleComment WHERE ArticleID = %d", (article_id,))
            result = cursor.fetchall()
            return result

    # -----------------------------------  Notification table methods ----------------------------------- #
    # Basic insertion into the Notification table
    def notification_insert(self, article_id, content, time):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO Notification (ArticleID, Content, Time) VALUES (%d, %s, %d)",
                           (article_id, content, time))
            self.mysql.connection.commit()

    # -----------------------------------  UserNotificationRead table methods ----------------------------------- #
    # Basic insertion into the UserNotificationRead table
    def user_notification_read_insert(self, user_id, notification_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO UserNotificationRead (UserID, NotificationID) VALUES (%d, %d)",
                           (user_id, notification_id))
            self.mysql.connection.commit()

    # Function to fetch all notifications of a user
    def user_notification_read_select_all_notifications(self, user_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM UserNotificationRead WHERE UserID = %d", (user_id,))
            result = cursor.fetchall()
            return result

    # Function to mark a notification as read for a user
    def user_notification_read_mark_read(self, user_notification_read_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE UserNotificationRead SET IsRead = 1 WHERE UserNotificationID = %d",
                           (user_notification_read_id,))
            self.mysql.connection.commit()

    # Function to fetch all unread notifications of a user
    def user_notification_read_select_unread(self, user_id):
        with self.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM UserNotificationRead WHERE UserID = %d AND IsRead = 0", (user_id,))
            result = cursor.fetchall()
            return result

