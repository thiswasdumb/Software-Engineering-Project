import datetime

import mysql.connector


class DataBaseConnection:
    """
    Here is how you can use this class to access its method for database manipulation
    all you have to do is to include these few lines at the beginning of your scripts:
        from database_connection import DataBaseConnection

        db = DataBaseConnection(
            host="localhost",
            user="root",
            passwd="",
            database="tradetalkerdb"
        )
    also, please check the "test_database_queries.py file to see how the methods are called, and how they return
    contact me if you need a function to change, or need a new function i.e. a different kind of access to database
    or other insertion/deletion etc.
    """
    def __init__(self, host, user, passwd, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        self.cursor = self.db.cursor()

    # -----------------------------------  User table methods ----------------------------------- #

    # test status: OK
    def user_insert_user(self, username: str, password: str, email: str, preferences=0) -> int:
        """
        Inserts into the user table
        :returns: user_id (int): the user_id of the user just added to the table
        """
        self.cursor.execute("INSERT INTO User (Username, Password, Email, Preferences) VALUES (%s, %s, %s, %s)",
                           (username, password, email, preferences))
        user_id = self.cursor.lastrowid
        self.db.commit()
        return user_id

    def user_select_by_id(self, user_id: int) -> list:
        """
        Selects a user by id
        :param user_id:
        :return: (id, username, passwd, email, preferences)
        """
        self.cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchone()
        return result

    def user_select_by_name(self, user_name: str) -> list:
        """
        Selects a user by name
        :param user_name:
        :return: (id, username, passwd, email, preferences)
        """
        self.cursor.execute("SELECT * FROM User WHERE UserName = %s", (user_name,))
        result = self.cursor.fetchone()
        return result

    # test status: OK
    def user_select_all(self) -> list:
        """
        Selects all user, returns in the form of a list of 5-tuples
        5-tuples : (id, username, passwd, email, preferences)
        :return:
        """
        self.cursor.execute("SELECT * FROM User")
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  Article table methods ----------------------------------- #

    # test status: OK
    def article_insert_article(self, title: str, company_name: str, content: str, publication_date: str, url: str, summary: str) -> int:
        """
        Inserts a single article in the article table
        :param title:
        :param company_name:
        :param content:
        :param publication_date:
        :param url:
        :param summary:
        :return: article_id (int): the article_id of the article just added to the table
        """
        company_id = self.company_get_company_id_by_name(company_name)[0]
        self.cursor.execute("INSERT INTO Article (Title, CompanyID, Content, PublicationDate, URL, Summary) VALUES "
                       "(%s, %s, %s, %s, %s, %s)",
                       (title, company_id, content, publication_date, url, summary))
        article_id = self.cursor.lastrowid
        self.db.commit()
        return article_id

    # test status: OK
    def article_select_all(self):
        """
        Returns all the article from the article table
        Returned object is a list of tuples each describing a company
        The tuple format: (article_id, company_id, title, content, pub_date, url, source, summary, score)
        :return:
        """
        self.cursor.execute("SELECT * FROM Article")
        result = self.cursor.fetchall()
        return result

    def article_select_by_company(self, company_name: str) -> list:
        """
        Returns all articles related to a company
        Returned object is a list of tuples each describing a company
        The tuple format: (article_id, company_id, title, content, pub_date, url, source, summary, score)
        :param company_name:
        :return:
        """
        company_id = self.company_get_company_id_by_name(company_name)[0]
        self.cursor.execute("SELECT * FROM Article WHERE CompanyID = %s", (company_id,))
        result = self.cursor.fetchall()
        return result

    def article_select_by_date(self, publication_date: datetime.date) -> list:
        """
        Returns all articles from a given date
        Returned object is a list of tuples each describing a company
        The tuple format: (article_id, company_id, title, content, pub_date, url, source, summary, score)
        :param publication_date:
        :return:
        """
        self.cursor.execute("SELECT * FROM Article WHERE PublicationDate = %s", (publication_date,))
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  Company table methods ----------------------------------- #

    # test status: OK
    def company_insert_company(self, company_name: str, stock_symbol: str, stock_price: float, industry: str, company_description: str)->int:
        """
        Inserts a company into the company table with necessary details
        :param company_name:
        :param stock_symbol:
        :param stock_price:
        :param industry:
        :param company_description:
        :return: company_id (int): the company_id of the company just added to the table
        """
        self.cursor.execute("INSERT INTO Company (CompanyName, StockSymbol, StockPrice, Industry, CompanyDescription, PredictedStockPrice, StockVariance, SentimentScore) "
                            "VALUES (%s, %s, %s, %s, %s, NULL, NULL, NULL)",
                           (company_name, stock_symbol, stock_price, industry, company_description))
        company_id = self.cursor.lastrowid
        self.db.commit()
        return company_id

    # test status: OK
    def company_select_all(self):
        """
        Returns all the companies in the company table
        Returns a list of tuples each representing a company
        The tuple format: (company_id, company_name, stock_symbol, stock_price, industry, company_description, predicted_stock_price, stock_variance, sentiment_score)
        :return:
        """
        self.cursor.execute("SELECT * FROM Company")
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def company_get_company_id_by_name(self, company_name: str) -> list:
        """
        Returns a list with one element, the id of the company with the name given as input
        use index-0 to access the id
        Does not consider non-existing companies, to be handled
        :param company_name:
        :return: (company_id,)
        """
        self.cursor.execute("SELECT CompanyID FROM Company WHERE CompanyName = %s", (company_name,))
        company_id = self.cursor.fetchone()
        return company_id

    # test status: OK
    def company_update_stock_price(self, company_name: str, stock_price: float) -> None:
        """
        Updates StockPrice
        :param company_name:
        :param stock_price:
        :return:
        """
        self.cursor.execute("UPDATE Company SET StockPrice = %s WHERE CompanyName = %s", (stock_price, company_name))
        self.db.commit()

    # test status: OK
    def company_update_predicted_stock_price(self, company_name: str, predicted_stock_price: float) -> None:
        """
        Updates PredictedStockPrice
        :param company_name:
        :param predicted_stock_price:
        :return:
        """
        self.cursor.execute("UPDATE Company SET PredictedStockPrice = %s WHERE CompanyName = %s", (predicted_stock_price,
                                                                                                  company_name))
        self.db.commit()

    # test status: OK
    def company_update_stock_variance(self, company_name: str, stock_variance: float) -> None:
        """
        Updates StockVariance
        :param company_name:
        :param stock_variance:
        :return:
        """
        self.cursor.execute("UPDATE Company SET StockVariance = %s WHERE CompanyName = %s", (stock_variance,
                                                                                            company_name))
        self.db.commit()

    # test status: OK
    def company_update_sentiment_score(self, company_name: str, sentiment_score: float) -> None:
        """
        Updates SentimentScore
        :param company_name:
        :param sentiment_score:
        :return:
        """
        self.cursor.execute("UPDATE Company SET SentimentScore = %s WHERE CompanyName = %s", (sentiment_score,
                                                                                             company_name))
        self.db.commit()

    # test status: OK
    def company_select_by_name(self, company_name: str) -> list:
        """
        Gives all the data of a company with the name passed as input
        Returns a tuple representing a company
        The tuple format: (company_id, company_name, stock_symbol, stock_price, industry, company_description, predicted_stock_price, stock_variance, sentiment_score)
        :param company_name:
        :return:
        """
        self.cursor.execute("SELECT * FROM Company WHERE CompanyName = %s", (company_name,))
        result = self.cursor.fetchone()
        return result

    # test status: OK
    def company_select_by_industry(self, industry: str) -> list:
        """
        Gives all data of all companies in a certain industry
        Returns a list of tuples each representing a company
        The tuple format: (company_id, company_name, stock_symbol, stock_price, industry, company_description, predicted_stock_price, stock_variance, sentiment_score)
        :param industry:
        :return:
        """
        self.cursor.execute("SELECT * FROM Company WHERE Industry = %s", (industry,))
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  Follow table methods ----------------------------------- #

    # test status: OK
    def follow_check(self, user_id: int, company_id: int) -> bool:
        """
        Checks if the following relation exists before the user and the company
        :param user_id:
        :param company_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM Follow WHERE UserID = %s AND CompanyID = %s", (user_id, company_id))
        result = self.cursor.fetchone()
        return result is not None

    # test status: OK
    def follow_toggle(self, user_id: int, company_id: int, follow_date: str) -> bool:
        """
        Toggles the following relation between the user and the company, returns the final state
        :param user_id:
        :param company_id:
        :param follow_date:
        :return:
        """
        is_following = self.follow_check(user_id, company_id)
        if is_following:
            self.cursor.execute("DELETE FROM Follow WHERE UserID = %s AND CompanyID = %s", (user_id, company_id))
        else:
            self.cursor.execute("INSERT INTO Follow (UserID, CompanyID, FollowDate) VALUES (%s, %s, %s)",
                           (user_id, company_id, follow_date))
        self.db.commit()
        # returning the final state as well -- can be previous, if needed for simplicity
        return not is_following

    # test status: OK
    def follow_select_all(self) -> list:
        """
        Selects all the following relationships in the table
        :return:
        """
        self.cursor.execute("SELECT * FROM Follow")
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def follow_get_user_following_companies(self, user_id: int) -> list:
        """
        Selects the company_id of all companies that the user is following
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT CompanyID FROM Follow WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        company_ids = []
        for res in result:
            company_ids.append(res[0])
        return company_ids

    def follow_get_company_followers(self, company_id: int) -> list:
        """
        Selects all the users that follow a certain company
        :param company_id:
        :return:
        """
        self.cursor.execute("SELECT UserID FROM Follow WHERE CompanyID = %s", (company_id,))
        result = self.cursor.fetchall()
        user_ids = []
        for res in result:
            user_ids.append(res[0])
        return user_ids

    # -----------------------------------  Like table methods ----------------------------------- #

    # test status: OK
    def like_relation_exists(self, user_id: int, article_id: int) -> bool:
        """
        Checks if the user has liked the article
        :param user_id:
        :param article_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM LikeTable Where UserID = %s AND ArticleID = %s", (user_id, article_id))
        result = self.cursor.fetchone()
        return result is not None

    # test status: OK
    def toggle_like(self, user_id: int, article_id: int) -> bool:
        """
        Toggles the liking relation between the user and the article, and returns the final state
        :param user_id:
        :param article_id:
        :return:
        """
        like_exists = self.like_relation_exists(user_id, article_id)
        if like_exists:
            self.cursor.execute(
                "DELETE FROM LikeTable WHERE UserID = %s AND ArticleID = %s", (user_id, article_id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO LikeTable (UserID, ArticleID) VALUES (%s, %s)", (user_id, article_id)
            )
        self.db.commit()
        # returning the result for further functionalities
        return not like_exists

    def like_get_user_liked_articles(self, user_id: int) -> list:
        """
        Returns a list of user's liked articles article_id
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT ArticleID FROM LikeTable  WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        return result


    # -----------------------------------  Bookmark table methods ----------------------------------- #

    # test status: OK
    def bookmark_relation_exists(self, user_id: int, article_id: int) -> bool:
        """
        Checks if the user has bookmarked the article
        :param user_id:
        :param article_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM Bookmark Where UserID = %s AND ArticleID = %s", (user_id, article_id))
        result = self.cursor.fetchone()
        return result is not None

    # test status: OK
    def toggle_bookmark(self, user_id: int, article_id: int) -> bool:
        """
        Toggles the bookmark relation between the user and the article, and returns the final state
        :param user_id:
        :param article_id:
        :return:
        """
        bookmark_exists = self.bookmark_relation_exists(user_id, article_id)
        if bookmark_exists:
            self.cursor.execute(
                "DELETE FROM Bookmark WHERE UserID = %s AND ArticleID = %s", (user_id, article_id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO Bookmark (UserID, ArticleID) VALUES (%s, %s)", (user_id, article_id)
            )
        self.db.commit()
        # returning the result for further functionalities
        return not bookmark_exists

    def bookmark_get_user_bookmarked_article(self, user_id: int) -> list:
        """
        Returns a list of user's bookmarked articles article_id
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT ArticleID FROM Bookmark WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  FAQ table methods ----------------------------------- #

    # test status: OK
    def faq_select_all(self) -> list:
        """
        Selects all FAQs in the table
        Returns all FAQs in a list of tuples, each representing one FAQ
        The tuple format: (faq_id, question, answer)
        :return:
        """
        self.cursor.execute("SELECT * FROM FAQ")
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def faq_insert_faq(self, question, answer):
        """
        Inserts a new FAQ to the table
        :param question:
        :param answer:
        :return:
        """
        self.cursor.execute("INSERT INTO FAQ (Question, Answer) VALUES (%s, %s)", (question, answer))
        self.db.commit()

    # -----------------------------------  UserQuestion table methods ----------------------------------- #

    # test status: OK
    def user_question_insert(self, user_id: int, question: str, time: str) -> int:
        """
        Insert a user query into the table
        :param user_id:
        :param question:
        :param time:
        :return: user_question_id (int): returns the user_question_id of the query just added to the table
        """
        self.cursor.execute("INSERT INTO UserQuestion (UserID, Question, Time) VALUES (%s, %s, %s)",
                                                                        (user_id, question, time))
        user_question_id = self.cursor.lastrowid
        self.db.commit()
        return user_question_id

    # test status: OK
    def user_question_mark_answered(self, user_question_id: int) -> None:
        """
        Marks a user question as answered in the table
        :param user_question_id:
        :return:
        """
        self.cursor.execute("UPDATE UserQuestion SET IsAnswered = 1 WHERE UserQuestionID = %s", (user_question_id,))
        self.db.commit()

    # test status: OK
    def user_question_select_all(self) -> list:
        """
        Selects all queries in the user question table
        :return:
        """
        self.cursor.execute("SELECT * FROM UserQuestion")
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def user_question_select_one_user_questions(self, user_id: int) -> list:
        """
        Returns all questions that a user has asked
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM UserQuestion WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  ArticleComment table methods ----------------------------------- #

    # test status: OK
    def article_comment_insert(self, user_id: int, article_id: int, content: str, time: str, parent_comment_id: int) ->int:
        """
        Inserts a comment for an article into the table, parent_comment_id is optional
        :param user_id:
        :param article_id:
        :param content:
        :param time:
        :param parent_comment_id:
        :return: article_comment_id (int): returns the article_comment_id for the comment just added to the table
        """
        if parent_comment_id:
            self.cursor.execute("INSERT INTO ArticleComment (UserID, ArticleID, Content, Time, ParentCommentID) "
                           "VALUES (%s, %s, %s, %s, %s)", (user_id, article_id, content, time, parent_comment_id))
        else:
            self.cursor.execute("INSERT INTO ArticleComment (UserID, ArticleID, Content, Time) "
                           "VALUES (%s, %s, %s, %s)", (user_id, article_id, content, time))
        article_comment_id = self.cursor.lastrowid
        self.db.commit()
        return article_comment_id

    # test status: OK
    def article_comment_select_by_article(self, article_id: int) -> list:
        """
        Selects all comments for an article
        :param article_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM ArticleComment WHERE ArticleID = %s", (article_id,))
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def article_comment_select_all(self) -> list:
        """
        Selects all comments for every article
        :return:
        """
        self.cursor.execute("SELECT * FROM ArticleComment")
        result = self.cursor.fetchall()
        return result

    # test status: OK
    def article_comment_select_by_user(self, user_id: int) -> list:
        """
        Selects all comments that a user has commented
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM ArticleComment WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  Notification table methods ----------------------------------- #
    # Basic insertion into the Notification table
    def notification_insert(self, article_id: int, content: str, time: str) -> int:
        """
        Inserts a notification into the table
        :param article_id:
        :param content:
        :param time:
        :return: notification_id (int): returns the notification_id of the notification just added to the table
        """
        self.cursor.execute("INSERT INTO Notification (ArticleID, Content, Time) VALUES (%s, %s, %s)",
                       (article_id, content, time))
        notification_id = self.cursor.lastrowid
        self.db.commit()
        return notification_id

    def notification_select_all(self) -> list:
        """
        Selects all the notifications in the table
        :return:
        """
        self.cursor.execute("SELECT * FROM Notification")
        result = self.cursor.fetchall()
        return result

    # -----------------------------------  UserNotificationRead table methods ----------------------------------- #
    # Basic insertion into the UserNotificationRead table
    def user_notification_read_insert(self, user_id: int, notification_id: int) -> None:
        """
        Inserts a new relation into the table
        :param user_id:
        :param notification_id:
        :return:
        """
        self.cursor.execute("INSERT INTO UserNotificationRead (UserID, NotificationID) VALUES (%s, %s)",
                       (user_id, notification_id))
        self.db.commit()

    # Function to fetch all notifications of a user
    def user_notification_read_select_all_notifications(self, user_id: int) -> list:
        """
        Selects every notification the user has received
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM UserNotificationRead WHERE UserID = %s", (user_id,))
        result = self.cursor.fetchall()
        return result

    # Function to mark a notification as read for a user
    def user_notification_read_mark_read(self, user_notification_read_id: int) -> None:
        """
        Marks a notification as read for the user
        :param user_notification_read_id:
        :return:
        """
        self.cursor.execute("UPDATE UserNotificationRead SET IsRead = 1 WHERE UserNotificationID = %s",
                       (user_notification_read_id,))
        self.db.commit()

    # Function to fetch all unread notifications of a user
    def user_notification_read_select_unread(self, user_id: int) -> list:
        """
        Selects every un-read notification that the user has
        :param user_id:
        :return:
        """
        self.cursor.execute("SELECT * FROM UserNotificationRead WHERE UserID = %s AND IsRead = 0", (user_id,))
        result = self.cursor.fetchall()
        return result
