class Link:

    def __init__(self, text, wikiquote_id):
        self.types=[]
        self.text = text
        self.wikiquote_id = wikiquote_id
        self.wikipedia_id = None
        self.wikidata_id = None
        self.prefix = None

    def print(self, level):
        print(" "*level + "Link: " + self.text + " -> " + str(self.types))