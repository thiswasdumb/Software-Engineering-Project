import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker')

from python_component.nltk_component.preprocessing import GetPOSClass, PreprocessText
from testing_articles import articles, articles_header  # Testing dictionary key=article, value= positive/neutral/negative (human classified)
from vader import SentimentAnalyser


class TestSentimentAnalyser(unittest.TestCase):
    def setUp(self):
        self.sample_tests = articles  # list of 10 articles 
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()

    def activation_function(self, compound_score:int):
        if compound_score > 0.5:
            return "positive"
        elif compound_score <= -0.5:
            return "negative"
        else:
            return "neutral"

    def test_each_article_sentiment(self):
        for article, expected_sentiment in self.sample_tests.items():
            # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
            with self.subTest():
                processed_news_article = self.preprocess_text.preprocess_text(article)
                test_compound_result = self.s.get_article_sentiment(processed_news_article)
                test_sentiment = self.activation_function(test_compound_result)
                
                # Assertions with a more informative message
                msg = f"For article: {articles_header[article]}. Expected: {expected_sentiment}, Got: {test_sentiment, test_compound_result}"
                print(msg)
                self.assertEqual(test_sentiment, expected_sentiment)



if __name__ == '__main__':
    unittest.main()
