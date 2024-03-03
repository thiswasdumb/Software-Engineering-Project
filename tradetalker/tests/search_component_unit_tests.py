import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker')

from python_component.nltk_component.search_component import ArticleSearch
from python_component.nltk_component import tf_idf 
from python_component.nltk_component.preprocessing import GetPOSClass, PreprocessText
from vader import SentimentAnalyser
from testing_articles import articles, articles_header, articles_list  # Testing dictionary key=article, value= positive/neutral/negative (human classified)
    


class TestSearchComponent(unittest.TestCase):

    def setUp(self):
        self.sample_tests = articles  # list of 10 articles 
        self.search_component = ArticleSearch(articles_list, articles_header) 
        get_pos_class = GetPOSClass() 
        self.preprocess_text = PreprocessText(get_pos_class)
        self.s = SentimentAnalyser()

    def activation_function(self, compound_score:int):
        if compound_score > 0.3:
            return "positive"
        elif compound_score <= -0.3:
            return "negative"
        else:
            return "neutral"

    def test_keywords(self):
        article_index = 1
        for article, expected_sentiment in self.sample_tests.items():
            # Mocking the external dependency for SentimentIntensityAnalyzer.polarity_scores
            article = self.preprocess_text.preprocess_text(article)
            with self.subTest():
                top_20_search_terms = self.search_component.tf_idf_object.get_top_n_terms(20, article_index).split(',')
                compound_score = 0 
                for word in top_20_search_terms:
                    compound_score += self.s.get_article_sentiment(word)['overall']
                test_result = self.activation_function(compound_score)
                self.assertEqual(test_result, expected_sentiment, msg=f"failed for article {article} where compound score was {compound_score}")
            article_index += 1 

if __name__ == '__main__':
    unittest.main()


