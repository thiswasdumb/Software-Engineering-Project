from newsapi import NewsApiClient
from newspaper import Article, ArticleException
from preprocessing import PreprocessText, GetPOSClass
from VADER import SentimentAnalyser

class GetNewsClass:
    def __init__(self, list_of_companies):
        """
        Initializes an instance of GetNewsClass.

        Parameters:
        - list_of_companies (list): A list of company names for which news articles will be fetched.
        Returns: 
        - None 
        """
        self.news_api = NewsApiClient(api_key='78c2cc21e0c04b9db286b7952f34a9f8')
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()

        self.all_articles = {}  # Dictionary with key = company, value = Dictionary obj returned from News API call
        for company in list_of_companies:
            self.all_articles[company] = self.news_api.get_everything(q=company,
                                                                     from_param='2024-02-10',
                                                                     language='en',
                                                                     sort_by='relevancy',
                                                                     page=1)

    def get_articles(self, company_name: str) -> None:
        """
        Fetches and processes news articles for a specific company.

        Parameters:
        - company_name (str): The name of the company for which news articles will be fetched.
        Returns:
        - None: all of the article data is stored onto the database
        """
        # Accessing articles
        articles = self.all_articles.get(company_name, {}).get('articles', [])
        
        # Process each article
        for article in articles:
            if company_name.lower().title() not in article['title']:
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
            
            except Exception as e:
                # Handle other exceptions
                continue
            
            article_company = company_name
            article_content = news_article.text
            processed_news_article = self.preprocess_text.preprocess_text(article_content)
            article_sentiment = self.s.get_article_sentiment(processed_news_article)
            article_title = article['title'] 
            article_summary = news_article.summary
            article_date = news_article.publish_date

            print(article_company, article_title, article_sentiment, article_summary, article_date)

    def get_all_articles(self):
        """
        Fetches and processes news articles for all companies specified during initialization.
        
        Parameters:
        - None
        Returns:
        - None: all of the article data is stored onto the database
        """
        for company in self.all_articles.keys():
            self.get_articles(company)

# Example usage
test = GetNewsClass(['google', 'microsoft', 'apple'])
test.get_all_articles()
