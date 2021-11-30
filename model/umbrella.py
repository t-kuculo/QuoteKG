from model.date_parsing_with_period import *

class umbrellaQuote:
    def __init__(self, QuoteObject):
        attributes = QuoteObject.__dict__

        #untemplated attributes

        self.section_titles = None
        self.id = None
        self.page_language = None
        self.entities = None
        self.contexts = None
        self.footnotes = None
        self.external_links = None
        self.segment_embeddings = None
        self.embedding = None
        self.date = None
        self.original = None
        self.direct_context = None
        self.quote_segments = None 
        self.quote = None
        self.language = None
        self.okay = None
        self.misattributed = None
        self.about = None
<<<<<<< HEAD
        self.wikiquote_id = None
        self.wikiquote_url = None
=======

>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        #templated attributes

        self.source = None
        self.cited = None
        self.comment = None
        self.translation = None
        self.author = None
        self.original = None
        self.release = None
        self.publisher = None
        self.url = None
        self.translators = None
        self.title = None
        self.surname = None
        self.location = None
        self.isbn = None
        self.publisher = None
        self.name = None
        self.year = None
        self.access_date = None
        self.release_date = None
        self.issn = None
        self.periodical = None
        self.month = None
        self.page = None
        self.referenced = None
        self.address = None
        self.publication = None
        self.explanation = None
        self.notes = None
        self.editor = None
        self.isbn = None
        self.archive_date = None
        self.archive_url = None
<<<<<<< HEAD

        #self.n_of_search_results = None
=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        
        for attr, value in attributes.items():
            setattr(self, attr, value)

        if (self.date == None) and (self.year or self.month):
            if self.year and not self.month:
                self.date = (self.year)
            elif self.year and self.month:
                self.date = (self.year,self.month)
        if self.date and type(self.date) is not tuple:
            self.date =  my_search_dates(str(self.date), self.page_language)

          

    def __bool__(self):
        return self.okay and not self.about
