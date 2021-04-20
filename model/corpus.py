from model.line import *
from model.complete_quote import *

class Corpus:   
    def __init__(self, completeQuotes):
        self.completeQuotes = dict()
        self.all_ids = set()
        for completeQuote in list(completeQuotes):
            self.completeQuotes.update({completeQuote.id:completeQuote})
            self.all_ids.update([completeQuote.id.split("_")[0]])
        self.all_ids = list(self.all_ids)


    def lookUp(self, wd_id, print=False):
        quotesById = []
        for quote_id in self.completeQuotes:
            if wd_id != quote_id.split("_")[0]:
                continue
            quotesById.append(self.completeQuotes[quote_id])
        if print:
            for completeQuote in quotesById:
                print([quote.quote for quote in completeQuote.quotes.values()])
                print("###\n")
            return quotesById
        else:
            return quotesById