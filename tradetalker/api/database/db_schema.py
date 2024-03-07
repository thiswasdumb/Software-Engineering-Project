"""Contains the database schema for the application, generated by sqlacodegen-v2."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
import yfinance as yf
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    text,
    update,
)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (  # type: ignore [attr-defined]
    Mapped,
    mapped_column,
    relationship,
)
from werkzeug.security import generate_password_hash

from linear_regression import Linear_Regression

db = SQLAlchemy()


class Company(db.Model):  # type: ignore [name-defined]
    """Contains the details of the companies in the database."""

    __tablename__ = "company"
    __table_args__ = (Index("stock_symbol_unique_index", "StockSymbol", unique=True),)

    CompanyID = mapped_column(Integer, primary_key=True)
    CompanyName = mapped_column(String(100, "utf8mb4_general_ci"), nullable=False)
    StockSymbol = mapped_column(String(10, "utf8mb4_general_ci"), nullable=False)
    StockPrice = mapped_column(Float, nullable=False)
    Industry = mapped_column(String(200, "utf8mb4_general_ci"), nullable=False)
    CompanyDescription = mapped_column(
        Text(collation="utf8mb4_general_ci"),
        nullable=False,
    )
    PredictedStockPrice = mapped_column(Float, nullable=True)
    StockVariance = mapped_column(Float, nullable=True)
    StockPrice_D_1 = mapped_column(Float, nullable=True)
    StockPrice_D_2 = mapped_column(Float, nullable=True)
    StockPrice_D_3 = mapped_column(Float, nullable=True)
    StockPrice_D_4 = mapped_column(Float, nullable=True)
    StockPrice_D_5 = mapped_column(Float, nullable=True)
    StockPrice_D_6 = mapped_column(Float, nullable=True)
    StockPrice_D_7 = mapped_column(Float, nullable=True)

    article: Mapped[list["Article"]] = relationship(
        "Article",
        uselist=True,
        back_populates="company",
    )
    follow: Mapped[list["Follow"]] = relationship(
        "Follow",
        uselist=True,
        back_populates="company",
    )

    def __init__(
        self,
        company_name: str,
        stock_symbol: str,
        stock_price: float,
        industry: str,
        company_description: str,
        predicted_stock_price: float | None,
        stock_variance: float | None,
        stock_price_d_1: float | None,
        stock_price_d_2: float | None,
        stock_price_d_3: float | None,
        stock_price_d_4: float | None,
        stock_price_d_5: float | None,
        stock_price_d_6: float | None,
        stock_price_d_7: float | None,
    ) -> None:
        """Initializes the company object."""
        self.CompanyName = company_name
        self.StockSymbol = stock_symbol
        self.StockPrice = stock_price
        self.Industry = industry
        self.CompanyDescription = company_description
        self.PredictedStockPrice = predicted_stock_price
        self.StockVariance = stock_variance
        self.StockPrice_D_1 = stock_price_d_1
        self.StockPrice_D_2 = stock_price_d_2
        self.StockPrice_D_3 = stock_price_d_3
        self.StockPrice_D_4 = stock_price_d_4
        self.StockPrice_D_5 = stock_price_d_5
        self.StockPrice_D_6 = stock_price_d_6
        self.StockPrice_D_7 = stock_price_d_7

    def to_dict(self) -> dict:
        """Converts a company to a dict object."""
        return {
            "id": self.CompanyID,
            "name": self.CompanyName,
            "symbol": self.StockSymbol,
            "stock_price": self.StockPrice,
            "industry": self.Industry,
            "description": self.CompanyDescription,
            "predicted_stock_price": self.PredictedStockPrice,
            "stock_variance": self.StockVariance,
            "stock_d1": self.StockPrice_D_1,
            "stock_d2": self.StockPrice_D_2,
            "stock_d3": self.StockPrice_D_3,
            "stock_d4": self.StockPrice_D_4,
            "stock_d5": self.StockPrice_D_5,
            "stock_d6": self.StockPrice_D_6,
            "stock_d7": self.StockPrice_D_7,
        }


class Faq(db.Model):  # type: ignore [name-defined]
    """Contains the frequently asked questions and their answers."""

    __tablename__ = "faq"

    FAQID = mapped_column(Integer, primary_key=True)
    Question = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    Answer = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)

    def __init__(self, question: str, answer: str) -> None:
        """Initializes the FAQ object."""
        self.Question = question
        self.Answer = answer


class User(UserMixin, db.Model):  # type: ignore [name-defined]
    """Contains the details of the users in the database."""

    __tablename__ = "user"
    __table_args__ = (
        Index("email_unique_index", "Email", unique=True),
        Index("username_unique_index", "Username", unique=True),
    )

    id = mapped_column(Integer, primary_key=True)
    Username = mapped_column(String(50, "utf8mb4_general_ci"), nullable=False)
    Password = mapped_column(String(200, "utf8mb4_general_ci"), nullable=False)
    Email = mapped_column(String(100, "utf8mb4_general_ci"), nullable=False)
    Preferences = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    IsVerified = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))

    follow: Mapped[list["Follow"]] = relationship(
        "Follow",
        uselist=True,
        back_populates="user",
    )
    userquestion: Mapped[list["UserQuestion"]] = relationship(
        "UserQuestion",
        uselist=True,
        back_populates="user",
    )
    articlecomment: Mapped[list["ArticleComment"]] = relationship(
        "ArticleComment",
        uselist=True,
        cascade="all, delete",
        back_populates="user",
    )
    bookmark: Mapped[list["Bookmark"]] = relationship(
        "Bookmark",
        uselist=True,
        back_populates="user",
    )
    liketable: Mapped[list["LikeTable"]] = relationship(
        "LikeTable",
        uselist=True,
        back_populates="user",
    )
    usernotificationread: Mapped[list["UserNotificationRead"]] = relationship(
        "UserNotificationRead",
        uselist=True,
        cascade="all, delete",
        back_populates="user",
    )

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
    ) -> None:
        """Initializes the user object."""
        self.Username = username
        self.Password = password
        self.Email = email

    def to_dict(self) -> dict:
        """Converts the user object to a dictionary."""
        return {
            "UserID": self.id,
            "Username": self.Username,
            "Password": self.Password,
            "Email": self.Email,
            "Preferences": self.Preferences,
            "IsVerified": self.IsVerified,
            "TempToken": self.TempToken,
        }

    def get_reset_token(self, expires_sec: int = 1800) -> str:
        """Generates a token for resetting the password."""
        return jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(UTC) + timedelta(seconds=expires_sec),
            },
            "secret_key",
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_token(token: str) -> int | None:
        """Verifies the token for resetting the password."""
        try:
            user_id = jwt.decode(token, "secret_key", algorithms=["HS256"])["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return user_id


class Article(db.Model):  # type: ignore [name-defined]
    """Contains the details of the articles in the database."""

    __tablename__ = "article"
    __table_args__ = (
        ForeignKeyConstraint(
            ["CompanyID"],
            ["company.CompanyID"],
            onupdate="CASCADE",
            name="company_article_fk",
        ),
        Index("company_article_fk", "CompanyID"),
    )

    ArticleID = mapped_column(Integer, primary_key=True)
    CompanyID = mapped_column(Integer, nullable=False)
    Title = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    Content = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    PublicationDate = mapped_column(DateTime, nullable=False)
    URL = mapped_column(String(300, "utf8mb4_general_ci"), nullable=False)
    Summary = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    PredictionScore = mapped_column(Float, nullable=False)
    KeyWords = mapped_column(String(100, "utf8mb4_general_ci"), nullable=True)
    ProcessedArticle = mapped_column(
        Text(collation="utf8mb4_general_ci"),
        nullable=True,
    )

    company: Mapped["Company"] = relationship("Company", back_populates="article")
    articlecomment: Mapped[list["ArticleComment"]] = relationship(
        "ArticleComment",
        uselist=True,
        back_populates="article",
    )
    bookmark: Mapped[list["Bookmark"]] = relationship(
        "Bookmark",
        uselist=True,
        back_populates="article",
    )
    liketable: Mapped[list["LikeTable"]] = relationship(
        "LikeTable",
        uselist=True,
        back_populates="article",
    )
    notification: Mapped[list["Notification"]] = relationship(
        "Notification",
        uselist=True,
        back_populates="article",
    )

    def __init__(
        self,
        company_id: int,
        title: str,
        content: str,
        publication_date: datetime,
        url: str,
        summary: str,
        prediction_score: float,
        processed_article: str | None,
    ) -> None:
        """Initializes the article object."""
        self.CompanyID = company_id
        self.Title = title
        self.Content = content
        self.PublicationDate = publication_date
        self.URL = url
        self.Summary = summary
        self.PredictionScore = prediction_score
        self.ProcessedArticle = processed_article


class Follow(db.Model):  # type: ignore [name-defined]
    """Contains the details of the companies that the users follow."""

    __tablename__ = "follow"
    __table_args__ = (
        ForeignKeyConstraint(
            ["CompanyID"],
            ["company.CompanyID"],
            name="company_follow_fk",
        ),
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_follow_fk"),
        Index("company_follow_fk", "CompanyID"),
        Index("user_follow_fk", "UserID"),
    )

    FollowID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    CompanyID = mapped_column(Integer, nullable=False)
    FollowDate = mapped_column(DateTime, nullable=False)

    company: Mapped["Company"] = relationship("Company", back_populates="follow")
    user: Mapped["User"] = relationship("User", back_populates="follow")

    def __init__(self, user_id: int, company_id: int) -> None:
        """Initializes the follow object."""
        self.UserID = user_id
        self.CompanyID = company_id
        self.FollowDate = datetime.now(UTC)


class UserQuestion(db.Model):  # type: ignore [name-defined]
    """Contains the questions that the users ask."""

    __tablename__ = "userquestion"
    __table_args__ = (
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_userq_fk"),
        Index("user_userq_fk", "UserID"),
    )

    UserQuestionID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    Question = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    Time = mapped_column(DateTime, nullable=False)
    IsAnswered = mapped_column(TINYINT(1), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="userquestion")

    def __init__(self, user_id: int, question: str) -> None:
        """Initializes the userquestion object."""
        self.UserID = user_id
        self.Question = question
        self.Time = datetime.now(UTC)
        self.IsAnswered = 0


class ArticleComment(db.Model):  # type: ignore [name-defined]
    """Contains the comments that the users post on the articles."""

    __tablename__ = "articlecomment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ArticleID"],
            ["article.ArticleID"],
            name="article_articlec_fk",
        ),
        ForeignKeyConstraint(
            ["ParentCommentID"],
            ["articlecomment.CommentID"],
            ondelete="CASCADE",
            name="parent_articlec_fk",
        ),
        ForeignKeyConstraint(
            ["UserID"],
            ["user.id"],
            ondelete="CASCADE",
            name="user_articlec_fk",
        ),
        Index("article_articlec_fk", "ArticleID"),
        Index("parent_articlec_fk", "ParentCommentID"),
        Index("user_articlec_fk", "UserID"),
    )

    CommentID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    ArticleID = mapped_column(Integer, nullable=False)
    Content = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    Time = mapped_column(DateTime, nullable=False)
    ParentCommentID = mapped_column(Integer)

    article: Mapped["Article"] = relationship(
        "Article",
        back_populates="articlecomment",
    )
    articlecomment: Mapped[Optional["ArticleComment"]] = relationship(
        "ArticleComment",
        remote_side=[CommentID],
        back_populates="articlecomment_reverse",
    )
    articlecomment_reverse: Mapped[list["ArticleComment"]] = relationship(
        "ArticleComment",
        uselist=True,
        remote_side=[ParentCommentID],
        back_populates="articlecomment",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="articlecomment",
        cascade="all, delete",
    )

    def __init__(
        self,
        user_id: int,
        article_id: int,
        content: str,
        parent_comment_id: int | None,
    ) -> None:
        """Initializes the articlecomment object."""
        self.UserID = user_id
        self.ArticleID = article_id
        self.Content = content
        self.Time = datetime.now(UTC)
        self.ParentCommentID = parent_comment_id


class Bookmark(db.Model):  # type: ignore [name-defined]
    """Contains the IDs of articles that the users bookmark."""

    __tablename__ = "bookmark"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ArticleID"],
            ["article.ArticleID"],
            name="article_bookmark_fk",
        ),
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_bookmark_fk"),
        Index("article_bookmark_fk", "ArticleID"),
        Index("user_bookmark_fk", "UserID"),
    )

    BookmarkID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    ArticleID = mapped_column(Integer, nullable=False)
    BookmarkDate = mapped_column(DateTime, nullable=False)

    article: Mapped["Article"] = relationship("Article", back_populates="bookmark")
    user: Mapped["User"] = relationship("User", back_populates="bookmark")

    def __init__(self, user_id: int, article_id: int) -> None:
        """Initializes the bookmark object."""
        self.UserID = user_id
        self.ArticleID = article_id
        self.BookmarkDate = datetime.now(UTC)


class LikeTable(db.Model):  # type: ignore [name-defined]
    """Contains the IDs of articles that the users like."""

    __tablename__ = "liketable"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ArticleID"],
            ["article.ArticleID"],
            name="article_like_fk",
        ),
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_like_fk"),
        Index("article_like_fk", "ArticleID"),
        Index("user_like_fk", "UserID"),
    )

    LikeID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    ArticleID = mapped_column(Integer, nullable=False)
    LikeDate = mapped_column(DateTime, nullable=False)

    article: Mapped["Article"] = relationship("Article", back_populates="liketable")
    user: Mapped["User"] = relationship("User", back_populates="liketable")

    def __init__(self, user_id: int, article_id: int) -> None:
        """Initializes the liketable object."""
        self.UserID = user_id
        self.ArticleID = article_id
        self.LikeDate = datetime.now(UTC)


class Notification(db.Model):  # type: ignore [name-defined]
    """Contains the notifications that the users receive."""

    __tablename__ = "notification"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ArticleID"],
            ["article.ArticleID"],
            name="article_notification_fk",
        ),
        Index("article_notification_fk", "ArticleID"),
    )

    NotificationID = mapped_column(Integer, primary_key=True)
    ArticleID = mapped_column(Integer, nullable=False)
    Content = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    Time = mapped_column(DateTime, nullable=False)

    article: Mapped["Article"] = relationship("Article", back_populates="notification")
    usernotificationread: Mapped[list["UserNotificationRead"]] = relationship(
        "UserNotificationRead",
        uselist=True,
        back_populates="notification",
    )

    def __init__(self, article_id: int, content: str) -> None:
        """Initializes the notification object."""
        self.ArticleID = article_id
        self.Content = content
        self.Time = datetime.now(UTC)


class UserNotificationRead(db.Model):  # type: ignore [name-defined]
    """Contains the IDs of notifications that the users have read."""

    __tablename__ = "usernotificationread"
    __table_args__ = (
        ForeignKeyConstraint(
            ["NotificationID"],
            ["notification.NotificationID"],
            name="notification_unr_fk",
        ),
        ForeignKeyConstraint(
            ["UserID"],
            ["user.id"],
            ondelete="CASCADE",
            name="user_unr_fk",
        ),
        Index("notification_unr_fk", "NotificationID"),
        Index("user_unr_fk", "UserID"),
    )

    UserNotificationReadID = mapped_column(Integer, primary_key=True)
    UserID = mapped_column(Integer, nullable=False)
    NotificationID = mapped_column(Integer, nullable=False)
    IsRead = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))

    notification: Mapped["Notification"] = relationship(
        "Notification",
        back_populates="usernotificationread",
    )
    user: Mapped["User"] = relationship("User", back_populates="usernotificationread")

    def __init__(self, user_id: int, notification_id: int) -> None:
        """Initializes the usernotificationread object."""
        self.UserID = user_id
        self.NotificationID = notification_id
        self.IsRead = 0


def add_data() -> None:
    """Adds initial data to the database."""
    user_list = [
        User(
            "User1",
            generate_password_hash("Password123!"),
            "user@gmail.com",
        ),
        User(
            "User2",
            generate_password_hash("Password1234!"),
            "user2@gmail.com",
        ),
    ]
    article_list = [
        Article(
            1,
            "The headline of Article 1",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            datetime.now(UTC),
            "URL1",
            "A short summary of the article.",
            0.5,
            None,
        ),
        Article(
            2,
            "The headline of Article 2",
            "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            datetime.now(UTC),
            "URL2",
            "Summary2",
            0.6,
            None,
        ),
    ]
    faq_list = [
        Faq(
            "What is TradeTalk?",
            "TradeTalk is a platform that provides users with the latest news and information about the stock market and companies. It also allows users to follow companies and receive notifications about them.",
        ),
        Faq(
            "How do I follow a company?",
            "To follow a company, simply search for the company using the search bar and click on the 'Follow' button on the company's page. You will then receive notifications about the company's news and updates.",
        ),
    ]
    notification_list = [
        Notification(
            1,
            "The content of notification 1.",
        ),
        Notification(
            2,
            "The content of notification 2.",
        ),
    ]
    user_notification_read_list = [
        UserNotificationRead(
            1,
            1,
        ),
        UserNotificationRead(
            2,
            2,
        ),
    ]
    article_comment_list = [
        ArticleComment(
            1,
            1,
            "This is a great comment.",
            None,
        ),
        ArticleComment(
            2,
            1,
            "This is another great comment.",
            1,
        ),
        ArticleComment(
            1,
            1,
            "This is a comment.",
            None,
        ),
        ArticleComment(
            2,
            2,
            "Another comment.",
            None,
        ),
    ]
    db.session.add_all(user_list)
    db.session.add_all(article_list)
    db.session.add_all(faq_list)
    db.session.add_all(notification_list)
    db.session.add_all(user_notification_read_list)
    db.session.add_all(article_comment_list)
    db.session.commit()


def add_base_company_data() -> None:
    """Adds initial data of the FTSE100 companies to the database."""
    symbols = [
        "III.L",
        "ADM.L",
        "AAF.L",
        "AAL.L",
        "ANTO.L",
        "AHT.L",
        "ABF.L",
        "AZN.L",
        "AUTO.L",
        "AV.L",
        "BME.L",
        "BA.L",
        "BARC.L",
        "BDEV.L",
        "BEZ.L",
        "BKG.L",
        "BP.L",
        "BATS.L",
        "BT-A.L",
        "BNZL.L",
        "BRBY.L",
        "CNA.L",
        "CCH.L",
        "CPG.L",
        "CTEC.L",
        "CRDA.L",
        "DCC.L",
        "DGE.L",
        "DPLM.L",
        "EDV.L",
        "ENT.L",
        "EXPN.L",
        "FCIT.L",
        "FLTR.L",
        "FRAS.L",
        "FRES.L",
        "GLEN.L",
        "GSK.L",
        "HLN.L",
        "HLMA.L",
        "HIK.L",
        "HWDN.L",
        "HSBA.L",
        "IHG.L",
        "IMI.L",
        "IMB.L",
        "INF.L",
        "ICP.L",
        "IAG.L",
        "ITRK.L",
        "JD.L",
        "KGF.L",
        "LAND.L",
        "LGEN.L",
        "LLOY.L",
        "LSEG.L",
        "MNG.L",
        "MKS.L",
        "MRO.L",
        "MNDI.L",
        "NG.L",
        "NWG.L",
        "NXT.L",
        "OCDO.L",
        "PSON.L",
        "PSH.L",
        "PSN.L",
        "PHNX.L",
        "PRU.L",
        "RKT.L",
        "REL.L",
        "RTO.L",
        "RMV.L",
        "RIO.L",
        "RR.L",
        "RS1.L",
        "SGE.L",
        "SBRY.L",
        "SDR.L",
        "SMT.L",
        "SGRO.L",
        "SVT.L",
        "SHEL.L",
        "SMDS.L",
        "SMIN.L",
        "SN.L",
        "SKG.L",
        "SPX.L",
        "SSE.L",
        "STAN.L",
        "STJ.L",
        "TW.L",
        "TSCO.L",
        "ULVR.L",
        "UU.L",
        "UTG.L",
        "VOD.L",
        "WEIR.L",
        "WTB.L",
        "WPP.L",
    ]
    companies = []
    for symbol in symbols:
        company = yf.Ticker(symbol)
        past_8_days_price = company.history(period="8d")["Close"].tolist()
        companies.append(
            Company(
                company.info.get("longName", "N/A"),  # CompanyName
                symbol,  # StockSymbol
                past_8_days_price[7],  # StockPrice
                company.info.get("industry", "N/A"),  # Industry
                company.info.get("longBusinessSummary", "N/A"),  # CompanyDescription
                None,  # PredictedStockPrice
                None,  # StockVariance
                past_8_days_price[6],  # StockPrice_D_1
                past_8_days_price[5],  # StockPrice_D_2
                past_8_days_price[4],  # StockPrice_D_3
                past_8_days_price[3],  # StockPrice_D_4
                past_8_days_price[2],  # StockPrice_D_5
                past_8_days_price[1],  # StockPrice_D_6
                past_8_days_price[0],  # StockPrice_D_7
            ),
        )

        db.session.add_all(companies)
        db.session.commit()


def company_daily_update(company: Company) -> None:
    """Performs the daily update of the companies."""
    try:
        ticker = yf.Ticker(company.StockSymbol)
        history = ticker.history(period="1d")
        if history.empty:
            # Handle the case where no data is returned
            logging.info("No data returned for %s", company.StockSymbol)
            return

        # Update stock price history
        # company.StockPrice_D_7 = company.StockPrice_D_6
        # company.StockPrice_D_6 = company.StockPrice_D_5
        # company.StockPrice_D_5 = company.StockPrice_D_4
        # company.StockPrice_D_4 = company.StockPrice_D_3
        # company.StockPrice_D_3 = company.StockPrice_D_2
        # company.StockPrice_D_2 = company.StockPrice_D_1
        # company.StockPrice_D_1 = company.StockPrice
        # company.StockPrice = history["Close"][-1]

        # ----- This is the part where we apply the prediction formula and calculate stock_variance and predicted_price
        # sentiment scores of the related articles for each company on the day
        articles = (
            Article.query.filter_by(CompanyID=company.CompanyID)
            .filter_by(PublicationDate=datetime.now(UTC))
            .all()
        )  # Check if the date format is the same as publication_date
        _sentiment_scores = [article.PredictionScore for article in articles]

        # variance calculations here
        # stock_variance = ... , uncomment when done
        company.StockVariance = None  # change to stock_variance
        # prediction calculations here
        # predicted_stock_price = ... , uncomment when done
        company.PredictedStockPrice = None  # change to predicted_stock_price

        # Commit changes to the database
        db.session.add(company)
        db.session.commit()
        logging.info("Stock price updated for %s", company.StockSymbol)
    except IntegrityError:
        # Handle any errors that occur during the update process
        logging.exception(
            "Error updating stock price for %s",
            company.StockSymbol,
        )
        db.session.rollback()  # Rollback changes in case of an error


def get_company_article_sentiment_scores(company_id: int) -> list:
    """Returns all the sentiment scores of the articles related to a company within the last n days."""
    articles = (
        db.session.execute(db.select(Article).filter_by(CompanyID=company_id))
        .scalars()
        .all()
    )
    print("#####")
    sentiment_scores = []
    for article in articles:
        print(article.Content)
        print(article.ArticleID)
        sentiment_scores.append(article.PredictionScore)
    print("sentiment scores: ", sentiment_scores)
    return sentiment_scores


def get_articles_by_company_name(company_name: str) -> list:
    """Returns all articles related to a company, for keyword analysis."""
    company = (
        db.session.execute(
            db.select(Company).filter(Company.CompanyName.like(f"%{company_name}%")),
        )
        .scalars()
        .first()
    )
    if not company:
        print("No result found for company named: ", company_name)
        return []

    articles = (
        db.session.execute(db.select(Article).filter_by(CompanyID=company.CompanyID))
        .scalars()
        .all()
    )
    if not articles:
        print("No articles found for the company ", company_name)
    return articles


def set_article_keywords(article_keywords_pairs: list[dict]) -> None:
    """Updates the keywords of articles in the database based on the provided pairs of article IDs and corresponding keywords.

    Args:
    ----
        article_keywords_pairs (list[dict]): List of dictionaries containing article ID as the key and keywords as the value.

    Raises:
    ------
        Any errors encountered during the execution will be propagated.

    """
    for article_keywords_pair in article_keywords_pairs:
        try:
            # Fixing the syntax errors
            db.session.execute(
                update(Article)
                .where(Article.ArticleID == article_keywords_pair.keys())
                .values(KeyWords=article_keywords_pair.values()),
            )
            db.session.commit()
        except IntegrityError as e:
            # Handle exceptions appropriately
            print(
                f"An error occurred in the member at article id {article_keywords_pair.keys()}: {e}",
            )


def get_article_from_news_script(article: dict) -> None:
    """Inserts the article recieved from the news script into the database."""
    # need the company_id first
    company = (
        db.session.execute(
            db.select(Company).filter(
                Company.CompanyName.like(f'%{article["Company"]}%'),
            ),
        )
        .scalars()
        .first()
    )
    if not company:
        print("Couldn't find the company name in the table for ", article["Company"])
        return
    print(company.CompanyID)

    new_article = Article(
        company_id=company.CompanyID,
        title=article["Title"],
        publication_date=article["PublicationDate"],
        url=article["URL"],
        summary=article["Summary"],
        prediction_score=article["PredictionScore"],
        content=article["Content"],
        processed_article=article["ProcessedArticle"],
    )
    db.session.add(new_article)
    db.session.commit()


def get_all_company_names() -> list:
    """Returns the name of all articles."""
    companies = db.session.execute(db.select(Company)).scalars().all()
    company_names = [company.CompanyName for company in companies]
    print(company_names)
    return company_names


def get_company_data_for_linear_regression(company: Company) -> dict:
    """Returns the data needed for our linear regression model in the form of a dict."""
    company_data = {"StockSymbol": company.StockSymbol}
    price_historic = [
        company.StockPrice_D_1,
        company.StockPrice_D_2,
        company.StockPrice_D_3,
        company.StockPrice_D_4,
        company.StockPrice_D_5,
    ]
    company_data["PriceHistoric"] = price_historic
    company_data["SentimentScores"] = get_company_article_sentiment_scores(
        company.CompanyID,
    )
    return company_data


def set_all_companies_predicted_price() -> None:
    """
    Sets the predicted_stock_price of all companies by running their data through the linear regression model
    to be called after the articles have been fetched.
    """
    try:
        companies = db.session.execute(db.select(Company)).scalars().all()
        for idx, company in enumerate(companies):
            try:
                predicted_stock_price = Linear_Regression.Linear_Regression(
                    company.StockSymbol, get_company_article_sentiment_scores(company.CompanyID), [
                        company.StockPrice_D_1, company.StockPrice_D_2, company.StockPrice_D_3, company.StockPrice_D_4, company.StockPrice_D_5
                    ])
                db.session.execute(
                    update(Company).where(Company.CompanyID == company.CompanyID)
                    .values(PredictedStockPrice=predicted_stock_price)
                )
                db.session.commit()
            except Exception as e:
                # Handle exceptions appropriately
                print(f"An error occurred in processing company with ID {company.CompanyID}: {e}")
    except Exception as ex:
        # Handle exceptions appropriately
        print(f"An error occurred while retrieving companies: {ex}")


def update_all_companies_daily() -> bool:
    """Updates daily stock prices for all companies."""
    try:
        companies = Company.query.all()
        for company in companies:
            company_daily_update(company)
        logging.info("Daily updates for all companies completed successfully.")
    except IntegrityError:
        logging.exception("Error updating daily stock prices")
        db.session.rollback()  # Rollback changes in case of an error
        return False
    return True
