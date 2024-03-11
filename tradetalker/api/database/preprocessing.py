"""Preprocesses text data for use in natural language processing models."""

import re
from collections import Counter

import nltk
from nltk import download
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class GetPOSClass:
    """Class to get the part of speech of a word. This is used by WordNet's
    WordNetLemmatizer for more accurate lemmatization.
    """

    def get_part_of_speech(self, word: str) -> str:
        """Gets the part of speech of the word."""
        try:
            probable_part_of_speech = wordnet.synsets(word)
        except LookupError:
            download("wordnet")
            probable_part_of_speech = wordnet.synsets(word)
        pos_counts = self._count_pos(probable_part_of_speech)
        return pos_counts.most_common(1)[0][0]

    def _count_pos(self, probable_part_of_speech: list) -> Counter:
        """Counts the part of speech of the word."""
        pos_counts: Counter = Counter()
        # The most common POS of the words sysnet is taken as the most probable
        for pos in ["n", "v", "a", "r"]:
            pos_counts[pos] = len(
                [item for item in probable_part_of_speech if item.pos() == pos],
            )
        return pos_counts


class PreprocessText:
    """Class to preprocess text data for use in natural language processing models."""

    def __init__(self, pos_classifier: GetPOSClass) -> None:
        """Initializes an instance of PreprocessText."""
        self.part_of_speech = pos_classifier
        try:
            self.stop_words = stopwords.words("english")
        except LookupError:
            download("stopwords")
            self.stop_words = stopwords.words("english")
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            download("punkt")
        self.normalizer = WordNetLemmatizer()

    def _clean_text(self, text: str) -> str:
        """Cleans the text."""
        return re.sub(r"\W+", " ", text).lower()

    def _normalize_token(self, token: str) -> str:
        """Normalizes the token."""
        return self.normalizer.lemmatize(
            token,
            self.part_of_speech.get_part_of_speech(token),
        )

    def preprocess_text(self, text: str) -> str:
        """Preprocesses the text."""
        cleaned = self._clean_text(text)
        tokenized = word_tokenize(cleaned)
        tokenized_wo_stopwords = [
            word for word in tokenized if word not in self.stop_words
        ]
        return " ".join(
            [
                self._normalize_token(token)
                for token in tokenized_wo_stopwords
                if not re.match(r"\d+", token)
            ],
        )
