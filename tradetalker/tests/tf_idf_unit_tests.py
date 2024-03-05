import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker')


from python_component.nltk_component.tf_idf import TF_IDF
from python_component.nltk_component.preprocessing import GetPOSClass, PreprocessText
from vader import SentimentAnalyser
from testing_articles import articles, articles_header, articles_list  # Testing dictionary key=article, value= positive/neutral/negative (human classified)
    


class TestTF_IDF(unittest.TestCase):
    #tests that the top n words returned by the function is accurate by 
    #by calculating their tf_idf scores and verifying that the words are ordered by highest tf_idf score (most important) to lowest 
    def setUp(self):
        self.sample_tests = articles  # list of 10 articles (preprocessed )
        self.tf_idf = TF_IDF(articles_list)
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()

    def test_keywords(self):
        article_id = 1 
        for article, expected_sentiment in self.sample_tests.items():
            # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
            with self.subTest():
                top_20_search_terms = self.tf_idf.get_top_n_terms(20, article_id).split(',')
                top_20_search_terms_scores = self.tf_idf.get_top_n_terms_tfidf_scores(20, article_id)
                print("Search terms:", top_20_search_terms)
                print("Search term scores:", top_20_search_terms_scores)
                self.assertTrue(all(top_20_search_terms_scores[i] >= top_20_search_terms_scores[i + 1] for i in range(len(top_20_search_terms_scores)-1)))
            article_id += 1

if __name__ == '__main__':
    unittest.main()

