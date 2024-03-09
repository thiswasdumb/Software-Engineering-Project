"""Class to summarise text using LSA summariser from sumy library."""

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer


class TextSummariser:
    """Class to summarise text using LSA summariser from sumy library."""

    def __init__(self, num_sentences: int = 2) -> None:
        """Initializes an instance of TextSummariser."""
        self.num_sentences = num_sentences
        self.summarizer = LsaSummarizer()

    def summarise(self, text: str) -> str:
        """Summarises the given text using LSA summariser from sumy library."""
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(parser.document, self.num_sentences)
        return " ".join([str(sentence) for sentence in summary])


# Example use
# test = TextSummarizer(2)
# print(test.summarise(text))
