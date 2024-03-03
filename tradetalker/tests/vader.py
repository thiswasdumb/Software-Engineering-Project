from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyser:

    def __init__(self):
        self.sent_int_analyzer = SentimentIntensityAnalyzer()

        
    def get_article_sentiment(self, processed_news_article: str) -> float:
        """
        Determines the sentiment possibilities of the article.
        Implements Sentiment Analysis from the NLTK module: https://www.nltk.org/howto/sentiment.html

        Arguments:
            - article: A string of pre-processed words in the article. 
        Returns:
            ---
        """

        sentiment = self.sent_int_analyzer.polarity_scores(processed_news_article) #A dictionaries of review sentiments which consists of compound, negative, neutral, and positive probablities.  
        return sentiment['compound']

