import sys 
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/python_component/nltk_component')


from search_articles_test import articles, articles_header
from preprocessing import GetPOSClass, PreprocessText
from sklearn.metrics.pairwise import polynomial_kernel
from tf_idf import TF_IDF



# Preprocess user query

get_pos_class = GetPOSClass() 
preprocess_text = PreprocessText(get_pos_class)


class ArticleSearch:
    def __init__(self, articles_list, articles_header):
        self.tf_idf_object = TF_IDF([preprocess_text.preprocess_text(a) for a in articles_list])
        self.articles = articles 
        self.articles_header = articles_header


    def search(self, search_term: str, relevance_score: float = 0.2):
        # Preprocess user query
        user_query = preprocess_text.preprocess_text(search_term)
        #User query vector 
        user_query_tfidf = self.tf_idf_object.vectorizer.transform([user_query])
        print("User query:", user_query_tfidf)
        # Calculate similarity between user query vector and the td_idf scores vector 
        similarities = polynomial_kernel(user_query_tfidf, self.tf_idf_object.tfidf_scores).flatten()
        print('Similarity:', similarities)

        # sort articles based on similarity - idx 1 in cosine_similarities[]. Highest score is more relevant
        article_ranking = sorted(list(enumerate(similarities)), key=lambda x: x[1], reverse=True)
        print("Article ranking", article_ranking)
        # Return relevant articles based on the threshold
        relevant_articles = [self.articles_header[id] for id, score in article_ranking if score >= relevance_score]
        return relevant_articles

# Example usage
search_component = ArticleSearch(articles, articles_header)
search_results = search_component.search("game")
print(search_results)

