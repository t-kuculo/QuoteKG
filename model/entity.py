class Entity:

    def __init__(self, wikiquoteId, wikiquotePageId):
        self.main_section = None
        self.wikiquote_id = wikiquoteId
        self.wikiquote_page_id = wikiquotePageId
        self.wikidata_id = None
        self.wikipedia_id = None
        self.types = []

    def print(self, level=0):
        print(self.wikiquote_id)

        print("Wikiquote Page ID: " + str(self.wikiquote_page_id))

        if self.wikipedia_id:
            print("Wikipedia ID: " + self.wikipedia_id)
        if self.wikidata_id:
            print("Wikidata ID: " + self.wikidata_id)

        if self.types:
            print("Types: " + str(self.types))

        if self.main_section:
            self.main_section.print(1)
