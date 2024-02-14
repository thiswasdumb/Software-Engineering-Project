from nltk.sentiment.vader import SentimentIntensityAnalyzer
from preprocessing import PreprocessText


class SentimentAnalyser:

    def __init__(self):
        self.sent_int_analyzer = SentimentIntensityAnalyzer()

        
    def get_article_sentiment(self, processed_news_article: str) -> dict:
        """
        Determines the sentiment possibilities of the article.
        Implements Sentiment Analysis from the NLTK module: https://www.nltk.org/howto/sentiment.html

        Arguments:
            - article: A string of pre-processed words in the article. 
w
        Returns:
            ---
        """

        sentiment = self.sent_int_analyzer.polarity_scores(processed_news_article) #A dictionaries of review sentiments which consists of compound, negative, neutral, and positive probablities.  
        output = {}
        output['pos'] = sentiment['pos'] * 100 
        output['neg'] = sentiment['neg'] * 100 
        output['neu'] = sentiment['neu'] * 100 
        output['overall'] = sentiment['compound'] 

        print("This text has an overall compound score of " + str(output['overall']) + "\nThe probability that the text is positive is " + str(output['pos']) + "%\nThe probability that the text is negative is " + str(output['neg']) + "%\nThe probability that the text is neutral is " + str(output['neu']) + "%")
        return output

