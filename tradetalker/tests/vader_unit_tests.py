import unittest
from unittest.mock import patch

#code below allows mac users to run tests from this directory, allows PATH to know where the dependencies are 
import sys
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/api')

from database.search_component import ArticleSearch
from database.tf_idf import TF_IDF 
from database.preprocessing import GetPOSClass, PreprocessText
from database.vader import SentimentAnalyser
from testing_articles import articles # Testing data,  article objects 
    


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
    
    def evaluate_article(self, article):
        test_vader_dict = self.s.get_article_sentiment(article.ProcessedArticle)
        test_sentiment = self.activation_function(test_vader_dict['overall'])
        return (test_sentiment, test_vader_dict)

    def perform_article_test(self, article_index):
        article = articles[article_index]
        test_sentiment, test_vader_dict = self.evaluate_article(article)
        msg = f"For subtest {article.ArticleID}: {article.header}. Expected: {article.sentiment}, Got: {test_sentiment} with sentiment score of {test_vader_dict['overall']}"
        print('----------------------------------------------------------------------')
        print(msg) 
        self.assertEqual(test_sentiment, article.sentiment, f"TEST FAILED FOR ARTICLE {article.header}")

    def test_article_0(self):
        self.perform_article_test(0)

    def test_article_1(self):
        self.perform_article_test(1)

    def test_article_2(self):
        self.perform_article_test(2)

    def test_article_3(self):
        self.perform_article_test(3)

    def test_article_4(self):
        self.perform_article_test(4)

    def test_article_5(self):
        self.perform_article_test(5)

    def test_article_6(self):
        self.perform_article_test(6)

    def test_article_7(self):
        self.perform_article_test(7)

    def test_article_8(self):
        self.perform_article_test(8)

    def test_article_9(self):
        self.perform_article_test(9)



    #single test using subtest context
    # def test_each_article_sentiment(self):
    #     i = 1
    #     for article in self.sample_tests:
    #         # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
    #         with self.subTest(article):
    #             test_vader_dict = self.s.get_article_sentiment(article.ProcessedArticle)
    #             test_sentiment = self.activation_function(test_vader_dict['overall'])
    #             msg = f"For subtest {article.ArticleID}: {article.header}. Expected: {article.sentiment}, Got: {test_sentiment} with sentiment score of {test_vader_dict['overall']}"
    #             print('----------------------------------------------------------------------')
    #             print(msg) 
    #             self.assertEqual(test_sentiment, article.sentiment, f"TEST FAILED FOR ARTICLE {article.header}")
    #             i += 1 


if __name__ == '__main__':
    unittest.main()
