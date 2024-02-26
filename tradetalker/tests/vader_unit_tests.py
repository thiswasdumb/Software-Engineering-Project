import unittest
from unittest.mock import patch
from ..python_component.Database.vader import SentimentAnalyser
from ...tradetalker.python_component.Database.preprocessing import PreprocessText, GetPOSClass  
from testing_articles import articles  # Testing dictionary key=article, value= positive/neutral/negative (human classified)

class TestSentimentAnalyser(unittest.TestCase):

    def setUp(self):
        self.sample_tests = articles  # list of 10 articles 
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()

    def activation_function(self, compound_score:int):
        if compound_score >= 0.5:
            return "positive"
        elif compound_score <= -0.5:
            return "negative"
        else:
            return "neutral"

    def test_each_article_sentiment(self):
        for article, expected_sentiment in self.sample_tests.items():
            # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
            with patch('vader.SentimentIntensityAnalyzer.polarity_scores') as mock_polarity_scores:
                mock_polarity_scores.return_value = {'compound': 0.5}  # Adjust the mock value as needed

                processed_news_article = self.preprocess_text(article)

                test_compound_result = self.s.get_article_sentiment(processed_news_article)['compound_score']
                test_sentiment = self.activation_function(test_compound_result)

                # Assertions with a more informative message
                msg = f"Failed for article: {article}. Expected: {expected_sentiment}, Got: {test_sentiment}"
                self.assertEqual(test_sentiment, expected_sentiment, msg=msg)

if __name__ == '__main__':
    unittest.main()
