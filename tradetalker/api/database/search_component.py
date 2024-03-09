"""Search component for articles. Uses TF-IDF to calculate similarity between user query and articles."""

import sys

from sklearn.metrics.pairwise import polynomial_kernel

from database.preprocessing import GetPOSClass, PreprocessText
from database.tf_idf import TFIDF

sys.path.insert(
    0,
    "/Users/mac/Documents/GitHub/SoftEngProject/tradetalker/python_component/nltk_component",
)

# from database.mock_article_objects import article_object_lists


# Preprocess user query

get_pos_class = GetPOSClass()
preprocess_text = PreprocessText(get_pos_class)

test_article_objects_list: list = []


class ArticleSearch:
    """Search component for articles. Uses TF-IDF to calculate similarity between user query and articles."""

    def __init__(self, article_objects_list: list) -> None:
        """Initializes the ArticleSearch class with the provided parameters."""
        converted = []
        for a in article_objects_list:
            new_dict = {}
            new_dict["ProcessedArticle"] = a.ProcessedArticle
            new_dict["ArticleID"] = a.ArticleID
            converted.append(new_dict)

        # print(converted, flush=True)

        self.tf_idf_object = TFIDF(converted)

        self.articles = article_objects_list
        # print(self.articles, flush=True)

        # dictionary to map article ID with their index in the self.articles list
        # used later to associate the calculated tf_idf scores with the article id and header
        self.articles_id = {}
        for i, article in enumerate(self.articles):
            self.articles_id[i] = article.ArticleID
        print(self.articles_id)


    def search(self, search_term: str, relevance_score: float = 0.2) -> list:
        """Searches for articles based on the user query. Returns a list of articles with their similarity scores."""
        # Preprocess user query
        user_query = preprocess_text.preprocess_text(search_term)
        # Calculate User query tf_idf vector
        user_query_tfidf = self.tf_idf_object.vectorizer.transform([user_query])
        # print("User query matrix:", user_query_tfidf)

        # Calculate similarity between user query vector and the td_idf scores vector
        similarities = polynomial_kernel(
            user_query_tfidf,
            self.tf_idf_object.tfidf_scores,
        ).flatten()
        # print("Similarity:", similarities)
        # sort articles based on similarity - idx 1 in the similarities[]. Highest score is more relevant
        article_ranking = sorted(
            enumerate(similarities),
            key=lambda x: x[1],
            reverse=True,
        )
        # print("Article ranking", article_ranking)

        # Map indices back to articles, select articles greater than a certain relevance score
        return [
            (self.articles_id[idx], score)
            for idx, score in article_ranking
            if score >= relevance_score
        ]


# Example usage
# search_component = ArticleSearch(article_object_lists)
# search_results = search_component.search("HSBC bank")
# print(search_results)
# for article, score in search_results:
#     print(f"Article ID: {article.ArticleID}, Header: {article.header}, Similarity Score: {score}")
