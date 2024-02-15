import pandas as pd
import numpy as np
# from articles import articles
from preprocessing import preprocess_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer 




class TF_IDF():
    def __init__(self, processed_articles: list[str]):
        # initialize and fit CountVectorizer
        self.count_vectorizer = CountVectorizer() 
        self.counts = self.count_vectorizer.fit_transform(processed_articles)

        # convert counts to tf-idf
        self.vectorizer = TfidfVectorizer(norm=None)

        # initialize and fit TfidfVectorizer
        self.tfidf_scores = self.vectorizer.fit_transform(processed_articles)


    def output(self):
        # get vocabulary of terms
        feature_names = self.vectorizer.get_feature_names()

        # get article index
        article_index = [f"Article {i+1}" for i in range(len(articles))]

        return pd.DataFrame(self.tfidf_scores.T.todense(), index=feature_names, columns=article_index)

    

# preprocessed articles, this will be the input for this module 
processed_articles = [preprocess_text(a) for a in articles]

tf_idf_object = TF_IDF(processed_articles)
df_tf_idf = tf_idf_object.output()

# get top 10 highest scoring tf-idf term for each article
for i in range(1, 3):  
    top_terms = df_tf_idf[[f'Article {i}']].nlargest(10, columns=[f'Article {i}'])
    print(f"\nTop 10 terms for Article {i}:\n{top_terms}")


