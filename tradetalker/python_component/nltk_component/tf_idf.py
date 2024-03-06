import pandas as pd
import numpy as np
from preprocessing import PreprocessText, GetPOSClass
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer 




class TF_IDF():
    def __init__(self, processed_article_objects: list):

        self.article_objects = processed_article_objects
        self.num_articles = len(processed_article_objects)
        self.df_tf_idf = None #to be calculated in _generate_tf_idf_matrix

        article_list = [a['ProcessedArticle'] for a in processed_article_objects]
        #dictionary to map article ID with matrix_index (the index in the tf_idf matrix)
        #used later to associate the calculated tf_idf scores with the article id 
        self.matrix_id = {}
        for i in range(len(article_list)):
            #key:  ArticleID      value:  i (from 0 to self.num_articles) 
            self.matrix_id[self.article_objects[i]['ArticleID']] = i 

        # initialize and fit TfidfVectorizer
        self.vectorizer = TfidfVectorizer(norm=None)
        self.tfidf_scores = self.vectorizer.fit_transform(article_list)
        #returns a matrix of form (row, column) tf_idf_score 
        #returns (i,j), where i = article_index, j = feature_index (each unique word)

        self.feature_names = self.vectorizer.get_feature_names_out()

        #generate the tf_idf matrix 
        self._generate_tf_idf_matrix()



    def _generate_tf_idf_matrix(self):
        # get article index array 
        article_index = [f"Article {i}" for i in range(self.num_articles)]
        self.df_tf_idf = pd.DataFrame(self.tfidf_scores.T.todense(), index=self.feature_names, columns=article_index)


    def get_top_n_terms_for_all_articles(self, top_n_words:int):
        for i in range(self.num_articles):
            article_obj = self.article_objects[i]
            matrix_id = self.matrix_id[article_obj['ArticleID']]
            top_n_words = self.get_top_n_terms(top_n_words, matrix_id)
            article_obj['KeyWords'] = top_n_words
        return self.article_objects
            

    def get_top_n_terms(self, n:int, matrix_id: int):
        #sorting the columns (each article) by their values (tf-idf score) for each term/word/feature
        top_terms = self.df_tf_idf[[f'Article {matrix_id}']].nlargest(n, columns=[f'Article {matrix_id}'])            
        #retrieving only the feature names (words)
        top_words = top_terms[[f'Article {matrix_id}']].index
        top_words_str = ",".join([w for w in top_words])
        return top_words_str
    

    def get_top_n_terms_tfidf_scores(self, n:int, matrix_id: int):
        #sorting the columns (each article) by their values (tf-idf score) for each term/word/feature
        top_terms = self.df_tf_idf[[f'Article {matrix_id}']].nlargest(n, columns=[f'Article {matrix_id}'])            
        #retrieving only the feature columns (tf_idf score)
        return top_terms[[f'Article {matrix_id}']].values.tolist()



#Example use case 
    
# tf_idf_object = TF_IDF(processed_articles)
# tf_idf_object.get_top_n_terms(10)




