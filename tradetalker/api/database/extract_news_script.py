import datetime
from flask import Flask
from newsapi import NewsApiClient
from newspaper import Article, ArticleException
from preprocessing import GetPOSClass, PreprocessText
from text_summariser import TextSummariser
from tf_idf import TF_IDF
from vader import SentimentAnalyser

app = Flask(__name__)



class GetNewsClass:
    article_id = 0

    def __init__(self, list_of_companies):
        """Initializes an instance of GetNewsClass.

        Parameters
        ----------
        - list_of_companies (list): A list (string) of company names for which news articles will be fetched.

        Returns
        -------
        - None
        """

        self.api_keys = ['Fb9cdea752a44045b9235bc4c5d69e12', '8968c158e1a44a5388312c35d8193541','Ee57dcf14e0a4903905440d1cdbed356']
        self.api_num = 0
        self.news_api = NewsApiClient(api_key=self.api_keys[self.api_num])
        get_pos_class = GetPOSClass()
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()
        self.t = TextSummariser(num_sentences=2)
        self.all_articles = {}
        #blacklisted websites (they require a paywall)
        self.black_listed = ['thefly.com']
        self.fetch_articles_from_api(list_of_companies)
        print(self.api_keys[self.api_num])


    def fetch_articles_from_api(self, list_of_companies: list):
        # Fetch articles for each company and store them in self.all_articles
        i = 0 
        while i < len(list_of_companies):
            try: 
                self.all_articles[list_of_companies[i]] = self.news_api.get_everything(
                    q=list_of_companies[i],
                    from_param="2024-03-01",
                    language="en",
                    sort_by="relevancy",
                    page=1,
                )
                i += 1 
            except Exception as e:
                self.alternate_api()
                print(f'Switching API key due to the following exception {e}')
                continue

    def alternate_api(self):
        self.api_num = (self.api_num + 1) % 3


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

        for company_name in self.all_articles.keys():
            article_dictionaries_for_one_company = self.get_articles(company_name)
            list_of_article_dictionaries.extend(article_dictionaries_for_one_company)


        # Calculate and insert tf_idf scores
        list_of_article_dictionaries = self.insert_tf_idf_scores(list_of_article_dictionaries)
        return list_of_article_dictionaries


    def get_articles(self, company_name: str) -> list[dict]:
        """Fetches and processes news articles for a specific company.

        Parameters
        ----------
        - company_name (str): The name of the company for which news articles will be fetched.

        Returns
        -------
        - A list of dictionaries, each dictionary is an article object for the company
        """
        list_of_article_dictionaries = []

        #to ensure no duplicates news articles are added
        seen_urls = set()
        

        articles = self.all_articles.get(company_name, {}).get("articles", [])

        for article in articles:
            article_title = article["title"]
            article_url = article["url"]

            #check if article has already been added, if so skip current article 
            if article_url.lower() in seen_urls or article_url in self.black_listed:
                continue

            seen_urls.add(article_url.lower())
            
            #filter out irrelevant articles
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
                "PublicationDate": news_article.publish_date
                if news_article.publish_date
                else datetime.datetime.now(),
                "KeyWords": None,  # Will be calculated later
            }
            print(article_object["PublicationDate"])

            GetNewsClass.article_id += 1
            list_of_article_dictionaries.append(article_object)


        return list_of_article_dictionaries


    def insert_tf_idf_scores(self, processed_articles: dict):
        if not processed_articles:
            print("No Articles")
            return processed_articles

        tf_idf = TF_IDF(processed_articles)
        return tf_idf.get_top_n_terms_for_all_articles(top_n_words=20)


# Example usage
test = GetNewsClass(["Ashtead"])
results = test.fetch_all_articles()
