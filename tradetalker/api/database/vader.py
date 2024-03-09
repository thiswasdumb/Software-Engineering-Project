"""Module to perform sentiment analysis on news articles."""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyser:
    """Class to perform sentiment analysis on news articles."""

    def __init__(self) -> None:
        """Initializes an instance of SentimentAnalyser."""
        try:
            nltk.data.find("sentiment/vader_lexicon")
        except LookupError:
            nltk.download("vader_lexicon")
        self.sent_int_analyzer = SentimentIntensityAnalyzer()

    def get_article_sentiment(self, processed_news_article: str) -> dict:
        """Determines the sentiment possibilities of the article.

        Implements Sentiment Analysis from the NLTK module: https://www.nltk.org/howto/sentiment.html.

        Parameters
        ----------
        processed_news_article : str
            A string of pre-processed words in the article.

        Returns
        -------
        dict
            A dictionary of the sentiment probabilities.

        """
        sentiment = self.sent_int_analyzer.polarity_scores(
            processed_news_article,
        )
        # A dictionary of review sentiments which consists of compound, negative,
        # neutral, and positive probablities.
        output = {}
        output["pos"] = sentiment["pos"] * 100
        output["neg"] = sentiment["neg"] * 100
        output["neu"] = sentiment["neu"] * 100
        output["overall"] = sentiment["compound"]

        return output
