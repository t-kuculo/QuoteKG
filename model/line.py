#from googletrans import Translator
#translator = Translator()

from nltk.sentiment import SentimentIntensityAnalyzer

class Line:

    def __init__(self):
        self.links = []
        self.templates = []
        self.sub_lines = []
        self.footnotes = []
        self.external_links = []
        self.text = None
        self.prefix = None
        self.italic = None
        self.bold = None
        """
        if self.text:
            sia = SentimentIntensityAnalyzer()
            self.language = (translator.detect(self.text).lang, translator.detect(self.text).confidence)
            translation = translator.translate(self.text)
            self.sentiment = sia.polarity_scores(translation.text)
        else:
            self.language = None
            self.sentiment = None
        """
        self.embedding = None

    def print(self, level, prefix="Line"):
        if self.text == None:
            self.text ="##None"
        print(" " * level + prefix + ": " + self.text)

        for link in self.links:
            link.print(level + 1)

        for template in self.templates:
            template.print(level + 1)

        for sub_line in self.sub_lines:
            sub_line.print(level + 1)

        for footnote in self.footnotes:
            print(" " * (level + 1) + "Footnote: " + footnote)

        for external_link in self.external_links:
            external_link.print(level + 1)
