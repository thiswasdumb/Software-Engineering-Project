from newsapi import NewsApiClient
from newspaper import Article, ArticleException
from preprocessing import PreprocessText, GetPOSClass
from vader import SentimentAnalyser
from flask import Flask
from tf_idf import TF_IDF
from text_summariser import TextSummariser


import datetime
import sys 

sys.path.insert(0,'/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/python_component')


app = Flask(__name__)

class GetNewsClass:
    article_id = 0 
    def __init__(self, list_of_companies):
        """
        Initializes an instance of GetNewsClass.

        Parameters:
        - list_of_companies (list): A list (string) of company names for which news articles will be fetched.
        Returns: 
        - None 
        """
        self.news_api = NewsApiClient(api_key='78c2cc21e0c04b9db286b7952f34a9f8')
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()
        self.t = TextSummariser(2)

        self.all_articles = {}  # Dictionary with key = company, value = Dictionary obj returned from News API call
        for company in list_of_companies:
            self.all_articles[company] = self.news_api.get_everything(
                q=company,
                from_param='2024-02-05',
                language='en',
                sort_by='relevancy',
                page=1)



    def fetch_all_articles(self) -> list[dict]:
        """
        Main function. 
        
        Fetches and processes news articles for all companies specified during initialization and puts them into a list of dict objects

        Then for each company's article corpus calculate the tf_idf matrix,
        for each article calculate the top 20 keywords using the words associated tf_idf scores 

        Parameters:
        - None
        Returns:
        - A list of dictionaries: each dictionary correlates to an article and all its attributes, to be inserted into the db 
        """
        #final output of the function
        list_of_article_dictionaries = []

        for company_name in self.all_articles.keys():    #self.all_articles keys are the company names 
            article_dictionaries_for_one_company = self.get_articles(company_name) #without keywords inserted 

            list_of_article_dictionaries.extend(article_dictionaries_for_one_company)

        article_dictionaries_with_keywords = self.insert_tf_idf_scores(list_of_article_dictionaries)
        #calculate and insert tf_idf scores
        list_of_article_dictionaries.extend(article_dictionaries_with_keywords)
        return list_of_article_dictionaries



    def get_articles(self, company_name: str) -> list[dict]:
        """
        Fetches and processes news articles for a specific company.

        Parameters:
        - company_name (str): The name of the company for which news articles will be fetched.
        Returns:
        - None: A list of dictionaries, each dictionary is an article object for the company
        """

        #final output of the function
        list_of_article_dictionaries = []

        # Accessing articles for the company from self.all_articles
        articles = self.all_articles.get(company_name, {}).get('articles', [])
    
        #dictionary to store the article data 
        article_object = {}

        for article in articles:
            article_title = article['title']
            if company_name.lower().title() not in article_title:
                continue
            # Get the URL of the article
            article_url = article['url']
            # Use newspaper3k to extract text content from the article URL
            news_article = Article(article_url)

            try: 
                news_article.download()
                news_article.parse()
            except ArticleException as e:
                print(f"Error downloading article: {e}")
                continue
            
            article_object['ArticleID'] = GetNewsClass.article_id #used to bookmark article objects, not used in actual db
            GetNewsClass.article_id += 1 
            article_object['Company'] = company_name
            article_object['Content'] = news_article.text
            article_object['ProcessedArticle'] = self.preprocess_text.preprocess_text(article_object['Content'])
            #sentiment analysis 
            article_object['PredictionScore'] = self.s.get_article_sentiment(article_object['ProcessedArticle'])['overall']
            article_object['Title'] = str(news_article.title)
            article_object['Summary'] = self.t.summarise(article_object['Content'])
            article_object['URL'] = str(article_url)
            article_object['PublicationDate'] = news_article.publish_date
            if not article_object['PublicationDate']:  # in some cases we got NULL date which would then prevent the insertion
                article_object['PublicationDate'] = datetime.datetime.now()

            print(article_object['Summary'], article_object['PredictionScore'])

            #Will be calculated later after the company article corpus is fully fetched 
            article_object['KeyWords'] = None 


            list_of_article_dictionaries.append(article_object)

        return list_of_article_dictionaries 
        


    def insert_tf_idf_scores(self,processed_articles: dict):
        #get the top 20 words 
        tf_idf = TF_IDF(processed_articles)
        return tf_idf.get_top_n_terms_for_all_articles(top_n_words=20)



#Function to be used in index 
    
# def insert_articles_and_keywords(company_names):
#     #initializing an instance of GetNewsClass
#     GetNewsClass = GetNewsClass(company_names)
#     #calling the main function to fetch, preprocess, carry out sentiment analysis for each article for each FTSE 100 company 
#     GetNewsClass.get_all_articles() 
#     #All company articles have already been inserted into the db. The tf_idf score can now be calculated



# Example usage
test = GetNewsClass(['coca-cola'])
results = test.fetch_all_articles()

results = [obj['Summary'] for obj in results]
# print("TEST RESULT:", results)


