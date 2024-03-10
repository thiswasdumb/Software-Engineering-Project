import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/api')

from database.search_component import ArticleSearch
from database.tf_idf import TFIDF 
from database.preprocessing import GetPOSClass, PreprocessText
from database.vader import SentimentAnalyser
from testing_articles import articles # Testing data,  article objects 
    

class TestTF_IDF(unittest.TestCase):
    #tests that the top n words returned by the function is accurate by 
    #by calculating their tf_idf scores and verifying that the words are ordered by highest tf_idf score (most important) to lowest 
    def setUp(self):
        converted = []
        for a in articles:
            new_dict = {}
            new_dict['ProcessedArticle'] = a.ProcessedArticle
            new_dict['ArticleID'] = a.ArticleID
            converted.append(new_dict)

        self.tf_idf = TFIDF(converted) #match input of tf-idf class, which are the article dictionary objects 
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()


    def perform_article_test(self, article_idx):
        print('----------------------------------------------------------------------')
        print(f' For subtest {article_idx+1}: For the following top 20 terms (only top 5 shown in log)')
        article = articles[article_idx]
        top_20_search_terms, top_20_search_terms_scores = self.evaluate_article(article)
        print("Search terms:", top_20_search_terms[:5])
        print("Search term scores:", top_20_search_terms_scores[:5])
        self.assertTrue(all(top_20_search_terms_scores[i] >= top_20_search_terms_scores[i + 1] for i in range(len(top_20_search_terms_scores)-1)))


    def evaluate_article(self, article):
        top_20_search_terms = self.tf_idf.get_top_n_terms(20, article.ArticleID-1).split(',')
        top_20_search_terms_scores = self.tf_idf.get_top_n_terms_tfidf_scores(20, article.ArticleID-1)
        return top_20_search_terms, top_20_search_terms_scores

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


    # def test_keywords(self):
    #     article_id = 0
    #     for article in articles:
    #         # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
    #         with self.subTest():
            #     print('----------------------------------------------------------------------')
            #     print(f' For subtest {article_id + 1}: For the following top 20 terms (only top 5 shown in log)')
            #     top_20_search_terms = self.tf_idf.get_top_n_terms(20, article_id).split(',')
            #     top_20_search_terms_scores = self.tf_idf.get_top_n_terms_tfidf_scores(20, article_id)
            #     print("Search terms:", top_20_search_terms[:5])
            #     print("Search term scores:", top_20_search_terms_scores[:5])
            #     self.assertTrue(all(top_20_search_terms_scores[i] >= top_20_search_terms_scores[i + 1] for i in range(len(top_20_search_terms_scores)-1)))
            # article_id += 1

if __name__ == '__main__':
    unittest.main()

