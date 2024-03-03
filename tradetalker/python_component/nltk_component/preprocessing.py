import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import random


class GetPOSClass:
    
    
    def get_part_of_speech(self, word: str) -> str:
        probable_part_of_speech = wordnet.synsets(word)
        pos_counts = self._count_pos(probable_part_of_speech)
        most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
        return most_likely_part_of_speech

    def _count_pos(self, probable_part_of_speech) -> Counter:
        pos_counts = Counter()
        #The most common pos of the words sysnet is taken as the most probable 
        for pos in ["n", "v", "a", "r"]:
            pos_counts[pos] = len([item for item in probable_part_of_speech if item.pos() == pos])
        return pos_counts



class PreprocessText:
    def __init__(self, pos_classifier: GetPOSClass) -> None:
        self.part_of_speech = pos_classifier
        self.stop_words = stopwords.words('english')
        self.normalizer = WordNetLemmatizer()

    def _clean_text(self, text: str) -> str:
        return re.sub(r'\W+', ' ', text).lower()

    def _normalize_token(self, token: str) -> str:
        return self.normalizer.lemmatize(token, self.part_of_speech.get_part_of_speech(token))
    
    def preprocess_text(self, text: str) -> str:
        cleaned = self._clean_text(text)
        tokenized = word_tokenize(cleaned)
        tokenized_wo_stopwords = [word for word in tokenized if word not in self.stop_words]
        normalized = " ".join([self._normalize_token(token) for token in tokenized_wo_stopwords if not re.match(r'\d+', token)])
        return normalized



