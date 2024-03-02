"""Contains the database schema for the application, generated by sqlacodegen-v2."""

from datetime import UTC, datetime
from typing import Optional

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
)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import (  # type: ignore [attr-defined]
    Mapped,
    mapped_column,
    relationship,
)
from werkzeug.security import generate_password_hash
import yfinance as yf

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
    PredictedStockPrice = mapped_column(Float, nullable=False)
    StockVariance = mapped_column(Float, nullable=False)
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
        predicted_stock_price: float,
        stock_variance: float,
    ) -> None:
        """Initializes the company object."""
        self.CompanyName = company_name
        self.StockSymbol = stock_symbol
        self.StockPrice = stock_price
        self.Industry = industry
        self.CompanyDescription = company_description
        self.PredictedStockPrice = predicted_stock_price
        self.StockVariance = stock_variance

    def to_dict(self) -> dict:
        """ Converts a company to a dict object """
        return {
            "CompanyID": self.CompanyID,
            "CompanyName": self.CompanyName,
            "StockSymbol": self.StockSymbol,
            "StockPrice": self.StockPrice,
            "Industry": self.Industry,
            "CompanyDescription": self.CompanyDescription,
            "PredictedStockPrice": self.PredictedStockPrice,
            "StockVariance": self.StockVariance,
            "StockPrice_D_1": self.StockPrice_D_1,
            "StockPrice_D_2": self.StockPrice_D_2,
            "StockPrice_D_3": self.StockPrice_D_3,
            "StockPrice_D_4": self.StockPrice_D_4,
            "StockPrice_D_5": self.StockPrice_D_5,
            "StockPrice_D_6": self.StockPrice_D_6,
            "StockPrice_D_7": self.StockPrice_D_7
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
    TempToken = mapped_column(String(100, "utf8mb4_general_ci"), nullable=True)

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
            "TempToken": self.TempToken
        }


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
    Source = mapped_column(String(100, "utf8mb4_general_ci"), nullable=False)
    Summary = mapped_column(Text(collation="utf8mb4_general_ci"), nullable=False)
    PredictionScore = mapped_column(Float, nullable=False)

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
        source: str,
        summary: str,
        prediction_score: float,
    ) -> None:
        """Initializes the article object."""
        self.CompanyID = company_id
        self.Title = title
        self.Content = content
        self.PublicationDate = publication_date
        self.URL = url
        self.Source = source
        self.Summary = summary
        self.PredictionScore = prediction_score


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
            name="parent_articlec_fk",
        ),
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_articlec_fk"),
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
    user: Mapped["User"] = relationship("User", back_populates="articlecomment")

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
        ForeignKeyConstraint(["UserID"], ["user.id"], name="user_unr_fk"),
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
            "Source1",
            "A short summary of the article.",
            0.5,
        ),
        Article(
            2,
            "The headline of Article 2",
            "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            datetime.now(UTC),
            "URL2",
            "Source2",
            "Summary2",
            0.6,
        ),
    ]
    company_list = [
        Company(
            "Company1",
            "CMP1",
            100,
            "Industry1",
            "Company1 is a pioneering force in the realm of technology solutions, dedicated to revolutionizing the digital landscape through cutting-edge innovation and unparalleled expertise. Founded on the principles of creativity, integrity, and excellence, Company1 has swiftly emerged as a trailblazer in the industry, setting new standards for technological advancement and customer satisfaction. At the heart of Company1's success lies a relentless commitment to pushing the boundaries of what's possible. With a team of visionary engineers, developers, and strategists at its helm, the company remains at the forefront of innovation, constantly exploring new avenues and embracing emerging technologies to deliver transformative solutions to its clients. From bespoke software development to state-of-the-art cloud computing services, Company1 offers a comprehensive suite of offerings tailored to meet the diverse needs of businesses across sectors. One of Company1's core strengths lies in its unwavering focus on delivering value-driven solutions that drive tangible results. By leveraging a combination of industry insights, technical expertise, and a customer-centric approach, the company works closely with clients to understand their unique challenges and goals, crafting bespoke strategies and solutions that empower them to thrive in an increasingly digital world. With a proven track record of success and a portfolio of satisfied clients, Company1 continues to set the benchmark for excellence in technology solutions, poised to lead the way into a future defined by innovation and opportunity.",
            100,
            10,
        ),
        Company(
            "Company2",
            "Symbol2",
            200,
            "Industry2",
            "Description2",
            200,
            20,
        ),
        Company(
            "Company3",
            "Symbol3",
            300,
            "Industry3",
            "Description3",
            300,
            30,
        ),
        Company(
            "Company4",
            "Symbol4",
            400,
            "Industry4",
            "Description4",
            400,
            40,
        ),
    ]
    faq_list = [
        Faq(
            "Question1",
            "Answer1",
        ),
        Faq(
            "Question2",
            "Answer2",
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
    db.session.add_all(company_list)
    db.session.add_all(faq_list)
    db.session.add_all(notification_list)
    db.session.add_all(user_notification_read_list)
    db.session.add_all(article_comment_list)
    db.session.commit()


def add_base_company_data() -> None:
    """ Adds initial data of the FTSE100 companies to the database """
    symbols = ['III.L', 'ADM.L', 'AAF.L', 'AAL.L', 'ANTO.L', 'AHT.L', 'ABF.L', 'AZN.L', 'AUTO.L', 'AV.L', 'BME.L',
               'BA.L', 'BARC.L', 'BDEV.L', 'BEZ.L', 'BKG.L', 'BP.L', 'BATS.L', 'BT-A.L', 'BNZL.L', 'BRBY.L', 'CNA.L',
               'CCH.L', 'CPG.L', 'CTEC.L', 'CRDA.L', 'DCC.L', 'DGE.L', 'DPLM.L', 'EDV.L', 'ENT.L', 'EXPN.L', 'FCIT.L',
               'FLTR.L', 'FRAS.L', 'FRES.L', 'GLEN.L', 'GSK.L', 'HLN.L', 'HLMA.L', 'HIK.L', 'HWDN.L', 'HSBA.L', 'IHG.L',
               'IMI.L', 'IMB.L', 'INF.L', 'ICP.L', 'IAG.L', 'ITRK.L', 'JD.L', 'KGF.L', 'LAND.L', 'LGEN.L', 'LLOY.L',
               'LSEG.L', 'MNG.L', 'MKS.L', 'MRO.L', 'MNDI.L', 'NG.L', 'NWG.L', 'NXT.L', 'OCDO.L', 'PSON.L', 'PSH.L',
               'PSN.L', 'PHNX.L', 'PRU.L', 'RKT.L', 'REL.L', 'RTO.L', 'RMV.L', 'RIO.L', 'RR.L', 'RS1.L', 'SGE.L',
               'SBRY.L', 'SDR.L', 'SMT.L', 'SGRO.L', 'SVT.L', 'SHEL.L', 'SMDS.L', 'SMIN.L', 'SN.L', 'SKG.L', 'SPX.L',
               'SSE.L', 'STAN.L', 'STJ.L', 'TW.L', 'TSCO.L', 'ULVR.L', 'UU.L', 'UTG.L', 'VOD.L', 'WEIR.L', 'WTB.L',
               'WPP.L']
    companies = []
    for symbol in symbols:
        company = yf.Ticker(symbol)
        past_8_days_price = company.history(period='8d')['Close'].tolist()
        companies.append(Company(
            company.info.get('longName', 'N/A'),  # CompanyName
            symbol,     # StockSymbol
            past_8_days_price[0],  # StockPrice
            company.info.get('industry', 'N/A'),  # Industry
            company.info.get('longBusinessSummary', 'N/A'),  # CompanyDescription
            None,  # PredictedStockPrice
            None,  # StockVariance
            past_8_days_price[1],  # StockPrice_D_1
            past_8_days_price[2],  # StockPrice_D_2
            past_8_days_price[3],  # StockPrice_D_3
            past_8_days_price[4],  # StockPrice_D_4
            past_8_days_price[5],  # StockPrice_D_5
            past_8_days_price[6],  # StockPrice_D_6
            past_8_days_price[7]   # StockPrice_D_7
        ))

        db.session.add_all(companies)
        db.session.commit()
