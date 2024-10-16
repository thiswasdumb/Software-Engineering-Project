"""Fetches news articles from NewsAPI and processes them for sentiment analysis and keyword extraction."""

from datetime import UTC, datetime

from flask import Flask
from newsapi import NewsApiClient
from newspaper import Article, ArticleException

from database.preprocessing import GetPOSClass, PreprocessText
from database.text_summariser import TextSummariser
from database.tf_idf import TFIDF
from database.vader import SentimentAnalyser

app = Flask(__name__)


class GetNewsClass:
    """Class to fetch news articles from NewsAPI and process them for sentiment analysis and keyword extraction."""

    article_id = 0

    def __init__(self, list_of_companies: list[str]) -> None:
        """Initializes an instance of GetNewsClass.

        Parameters
        ----------
        list_of_companies : list
            A list (string) of company names for which news articles will be fetched.

        Returns
        -------
        None

        """
        self.api_keys = [
            "6948843a4d3b4c2f951df0279868613d",
            "51bdd78bd260400b864a9152e38d3a5f",
            "9256e34369fb4a259418bb28cb0e9843",
            "Fb9cdea752a44045b9235bc4c5d69e12",
            "8968c158e1a44a5388312c35d8193541",
            "Ee57dcf14e0a4903905440d1cdbed356",
            "78c2cc21e0c04b9db286b7952f34a9f8",
            "856923ce4cc34541b8815df3c2265878",
            "F90a2f0d38714c18b4ad0e5a991fa558",
            "a72e7943397b482b90543d57a1e3aaba",
        ]
        self.api_num = 0
        self.news_api = NewsApiClient(api_key=self.api_keys[self.api_num])
        get_pos_class = GetPOSClass()
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()
        self.t = TextSummariser(num_sentences=2)
        self.all_articles: dict = {}
        # blacklisted websites (they require a paywall)
        self.black_listed = ["thefly.com", "tmonews.com"]
        self.fetch_articles_from_api(list_of_companies)

    def check_if_blacklisted(self, url_to_check: str) -> bool:
        """Checks if a URL is blacklisted."""
        return any(domain in url_to_check for domain in self.black_listed)

    def fetch_articles_from_api(self, list_of_companies: list) -> None:
        """Fetches news articles from the NewsAPI for each company in the list."""
        # Fetch articles for each company and store them in self.all_articles
        i = 0
        while i < len(list_of_companies):
            try:
                self.all_articles[list_of_companies[i]] = self.news_api.get_everything(
                    q=list_of_companies[i],
                    from_param="2024-03-05",
                    language="en",
                    sort_by="relevancy",
                    page=1,
                )
                i += 1
            except Exception as e:
                self.alternate_api()
                print(f"Switching API key due to the following exception {e}")
                i += 1

    def alternate_api(self) -> None:
        """Switches to the next API key."""
        self.api_num = (self.api_num + 1) % 10

    def fetch_all_articles(self) -> list[dict]:
        """Main function.

        Fetches and processes news articles for all companies specified during initialization and puts them into a list of dict objects.

        Then for each company's article corpus calculate the tf_idf matrix,
        for each article calculate the top 20 keywords using the words associated tf_idf scores.

        Returns
        -------
        - A list of dictionaries: each dictionary correlates to an article and all its attributes, to be inserted into the db

        """
        list_of_article_dictionaries = []

        for (
            company_name
        ) in self.all_articles:  # self.all_articles are the company names
            article_dictionaries_for_one_company = self.get_articles(
                company_name,
            )  # without keywords inserted

            list_of_article_dictionaries.extend(article_dictionaries_for_one_company)

        # Calculate and insert tf_idf scores
        return self.insert_tf_idf_scores(list_of_article_dictionaries)

    def get_articles(self, company_name: str) -> list[dict]:
        """Fetches and processes news articles for a specific company.

        Parameters
        ----------
        company_name : str
            The name of the company for which news articles will be fetched.

        Returns
        -------
        list[dict]
            A list of dictionaries. Each dictionary is an article object for the company.

        """
        list_of_article_dictionaries = []

        # to ensure no duplicates news articles are added
        seen_urls = set()

        articles = self.all_articles.get(company_name, {}).get("articles", [])

        for article in articles:
            article_title = article["title"]
            article_url = article["url"]

            # check if article has already been added, if so skip current article
            if article_url.lower() in seen_urls or self.check_if_blacklisted(
                article_url,
            ):
                continue

            seen_urls.add(article_url.lower())

            # filter out irrelevant articles
            if company_name.lower() not in article_title.lower():
                continue

            news_article = Article(article_url)

            try:
                news_article.download()
                news_article.parse()
            except ArticleException as e:
                print(f"Error downloading article: {e}")
                continue

            article_object = {
                "ArticleID": GetNewsClass.article_id,
                "Company": company_name,
                "Content": news_article.text,
                "ProcessedArticle": self.preprocess_text.preprocess_text(
                    news_article.text,
                ),
                "PredictionScore": self.s.get_article_sentiment(
                    news_article.text,
                )["overall"],
                "Title": str(news_article.title),
                "Summary": self.t.summarise(news_article.text),
                "URL": str(article_url),
                "PublicationDate": (
                    news_article.publish_date
                    if news_article.publish_date
                    else datetime.now(UTC)
                ),
                "KeyWords": None,  # Will be calculated later
            }

            GetNewsClass.article_id += 1
            list_of_article_dictionaries.append(article_object)

        return list_of_article_dictionaries

    def insert_tf_idf_scores(self, processed_articles: list) -> list:
        """Calculates and inserts tf_idf scores for each article in the list."""
        if len(processed_articles) <= 0:
            print("No Articles")
            return processed_articles
        # get the top 20 words
        tf_idf = TFIDF(processed_articles)
        return tf_idf.get_top_n_terms_for_all_articles(top_n_words=20)


# Example usage
# test = GetNewsClass(["Ashtead"])
# results = test.fetch_all_articles()
