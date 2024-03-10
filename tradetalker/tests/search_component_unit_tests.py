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
    


class TestSearchComponent(unittest.TestCase):

    def setUp(self):
        self.sample_tests = articles  # list of 10 articles 
        self.search_component = ArticleSearch(articles) 
        self.s = SentimentAnalyser()

    def activation_function(self, compound_score:int):
        if compound_score > 0.3:
            return "positive"
        elif compound_score <= -0.3:
            return "negative"
        else:
            return "neutral"

    def test_article_0_keywords(self):
        self.perform_article_keywords_test(0)
    
    def test_article_0_search(self):
        self.perform_article_search_test(0, 'data centre')

    def test_article_1_keywords(self):
        self.perform_article_keywords_test(1)
    
    def test_article_1_search(self):
        self.perform_article_search_test(1, 'xbox hardware')

    def test_article_2_keywords(self):
        self.perform_article_keywords_test(2)
    
    def test_article_2_search(self):
        self.perform_article_search_test(2, 'apple car')

    def test_article_3_keywords(self):
        self.perform_article_keywords_test(3)

    def test_article_3_search(self):
        self.perform_article_search_test(3, 'lawsuit')
    
    def test_article_4_keywords(self):
        self.perform_article_keywords_test(4)

    def test_article_4_search(self):
        self.perform_article_search_test(4, 'ready meal sick')

    def test_article_5_keywords(self):
        self.perform_article_keywords_test(5)

    def test_article_5_search(self):
        self.perform_article_search_test(5, 'defense aircraft engines')

    def test_article_6_keywords(self):
        self.perform_article_keywords_test(6)

    def test_article_6_search(self):
        self.perform_article_search_test(6, 'jd sports')

    def test_article_7_keywords(self):
        self.perform_article_keywords_test(7)

    def test_article_7_search(self):
        self.perform_article_search_test(7, "vaccines")

    def test_article_8_keywords(self):
        self.perform_article_keywords_test(8)
    
    def test_article_8_search(self):
        self.perform_article_search_test(8, "shipments")

    def test_article_9_keywords(self):
        self.perform_article_keywords_test(9)

    def test_article_9_search(self):
        self.perform_article_search_test(9, "prudential")

    def perform_article_search_test(self, article_idx, user_search_term):
        article = articles[article_idx]
        relevant_articles = self.search_component.search(user_search_term)
        top_article_id = relevant_articles[0][0]
        top_article = articles[top_article_id-1] #id = index -1 
        print('----------------------------------------------------------------------')
        print(f"Running search subtest {article_idx+1} for the following article: {article.header}")
        print("Expected:", article.header , "Got:", top_article.header)
        self.assertEqual(top_article.header, article.header, msg=f"FAILED FOR: {article.header} where top search result was {top_article.header}")


    def perform_article_keywords_test(self, article_index):
        article = articles[article_index]
        top_20_search_terms = self.search_component.tf_idf_object.get_top_n_terms(20, article_index).split(',')
        compound_score = 0
        for word in top_20_search_terms:
            compound_score += self.s.get_article_sentiment(word)['overall']
            test_result = self.activation_function(compound_score)
        print('----------------------------------------------------------------------')
        print(f"Running subtest {article_index+1} for the following article: {article.header}")
        print("Test Result:", test_result, "Expected:", article.sentiment)
        self.assertEqual(test_result, article.sentiment, msg=f"FAILED FOR: {article.header} where compound score was {compound_score}")


    #single test using subtest context
    # def test_keywords(self):
    #     for article_index, article in enumerate(self.sample_tests):
    #         with self.subTest(article=article):
    #             top_20_search_terms = self.search_component.tf_idf_object.get_top_n_terms(20, article_index).split(',')
    #             compound_score = 0
    #             for word in top_20_search_terms:
    #                 compound_score += self.s.get_article_sentiment(word)['overall']
    #             test_result = self.activation_function(compound_score)
    #             print('----------------------------------------------------------------------')
    #             print(f"Running subtest {article_index+1} for the following article: {article.header}")
    #             print("Test Result:", test_result, "Expected:", article.sentiment)
    #             self.assertEqual(test_result, article.sentiment, msg=f"failed for article {article} where compound score was {compound_score}")

if __name__ == '__main__':
    unittest.main()


