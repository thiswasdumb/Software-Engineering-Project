from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer


class TextSummariser:
    def __init__(self, num_sentences=2):
        self.num_sentences = num_sentences
        self.summarizer = LsaSummarizer()

    def summarise(self, text: str) -> str:
        self.parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(self.parser.document, self.num_sentences)
        return " ".join([str(sentence) for sentence in summary])


# Example use
# test = TextSummarizer(2)
# print(test.summarise(text))
