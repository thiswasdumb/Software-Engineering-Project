import pandas as pd
import numpy as np
from search_articles_test import articles
from preprocessing import PreprocessText, GetPOSClass
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer 




class TF_IDF():
    def __init__(self, processed_articles: list[str]):
        # convert counts to tf-idf
        self.num_articles = len(processed_articles)
        self.vectorizer = TfidfVectorizer(norm=None)
        # initialize and fit TfidfVectorizer
        self.tfidf_scores = self.vectorizer.fit_transform(processed_articles)
        #returns a matrix of form (row, column) tf_idf_score 
        #returns (i,j), where i = article_index, j = feature_index (each unique word)
        self.feature_names = self.vectorizer.get_feature_names_out()
        #generate the tf_idf matrix 
        self._generate_tf_idf_matrix()

    def _generate_tf_idf_matrix(self):
        # get article index array 
        article_index = [f"Article {i+1}" for i in range(self.num_articles)]
        self.df_tf_idf = pd.DataFrame(self.tfidf_scores.T.todense(), index=self.feature_names, columns=article_index)


    def get_top_n_terms(self, n:int):
        for i in range(1, self.num_articles+1):  
            top_terms = self.df_tf_idf[[f'Article {i}']].nlargest(n, columns=[f'Article {i}'])            
            # print(top_terms)
            top_words =  top_terms[f'Article {i}']
            print(top_words)
            print(top_words.to_list())


get_pos_class = GetPOSClass() 
preprocess_text = PreprocessText(get_pos_class)
# preprocessed articles, this will be the input for this module 
processed_articles = [preprocess_text.preprocess_text(a) for a in articles.keys()]

tf_idf_object = TF_IDF(processed_articles)
tf_idf_object.get_top_n_terms(10)




