import sys 
sys.path.insert(0, '/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/python_component/nltk_component')


from preprocessing import GetPOSClass, PreprocessText
from sklearn.metrics.pairwise import polynomial_kernel
from tf_idf import TF_IDF
from mock_article_objects import article_object_lists


# Preprocess user query

get_pos_class = GetPOSClass() 
preprocess_text = PreprocessText(get_pos_class)


class ArticleSearch:
    def __init__(self, article_objects_list):
        self.tf_idf_object = TF_IDF([a.processed_content for a in article_objects_list])

        self.articles = article_objects_list 

        #dictionary to map article ID with their index in the self.articles list 
        #used later to associate the calculated tf_idf scores with the article id and header 
        self.articles_id = {}
        for i in range(len(self.articles)):
            self.articles_id[i] = self.articles[i].ArticleID 


    def search(self, search_term: str, relevance_score: float = 0.2):
        # Preprocess user query
        user_query = preprocess_text.preprocess_text(search_term)
        #Calculate User query tf_idf vector 
        user_query_tfidf = self.tf_idf_object.vectorizer.transform([user_query])
        print("User query matrix:", user_query_tfidf)

        # Calculate similarity between user query vector and the td_idf scores vector 
        similarities = polynomial_kernel(user_query_tfidf, self.tf_idf_object.tfidf_scores).flatten()
        print('Similarity:', similarities)
        # sort articles based on similarity - idx 1 in the similarities[]. Highest score is more relevant
        article_ranking = sorted(list(enumerate(similarities)), key=lambda x: x[1], reverse=True)
        print("Article ranking", article_ranking)

        # Map indices back to articles, select articles greater than a certain relevance score
        relevant_articles = [(self.articles_id[idx], score) for idx, score in article_ranking if score >= relevance_score]
        return relevant_articles

# Example usage
search_component = ArticleSearch(article_object_lists)
search_results = search_component.search("AI")
print(search_results)
# for article, score in search_results:
#     print(f"Article ID: {article.ArticleID}, Header: {article.header}, Similarity Score: {score}")

