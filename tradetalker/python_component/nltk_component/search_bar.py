from sklearn.metrics.pairwise import linear_kernel
from tf_idf import TF_IDF
from search_articles_test import articles, articles_header
from preprocessing import GetPOSClass, PreprocessText
from sklearn.metrics.pairwise import polynomial_kernel


# Preprocess user query

get_pos_class = GetPOSClass() 
preprocess_text = PreprocessText(get_pos_class)


class ArticleCosineSearch:
    def __init__(self, articles):
        self.tf_idf_object = TF_IDF([preprocess_text.preprocess_text(a) for a in articles.keys()])

    def search(self, search_term: str, relevance_score: float = 0.2):
        # Preprocess user query
        user_query = preprocess_text.preprocess_text(search_term)
        #User query vector 
        user_query_tfidf = self.tf_idf_object.vectorizer.transform([user_query])
        print("User query:", user_query_tfidf)
        # Calculate cosine similarity
        cosine_similarities = polynomial_kernel(user_query_tfidf, self.tf_idf_object.tfidf_scores).flatten()
        print('Cosine similarity:', cosine_similarities)
        # sort articles based on similarity - idx 1 in cosine_similarities[]. Highest score is more relevant
        article_ranking = sorted(list(enumerate(cosine_similarities)), key=lambda x: x[1], reverse=True)
        print("Article ranking", article_ranking)
        # Return relevant articles based on the threshold
        relevant_articles = [articles_header[index] for index, score in article_ranking if score >= relevance_score]
        return relevant_articles

# Example usage
search_component = ArticleCosineSearch(articles)
search_results = search_component.search("game")
print(search_results)

