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


    def lookUp(self, wd_id, printout=False):
        quotesById = []
        for quote_id in self.completeQuotes:
            if wd_id != quote_id.split("_")[0]:
                quotesById.append(self.completeQuotes[quote_id])
        if printout:
            for completeQuote in quotesById:
                print([quote.quote for quote in list(completeQuote.quotes.values())[0]])
                print("###\n")
            return quotesById
        else:
            return quotesById


def lookUp(c, wd_id, printout=False):
    quotesById = []
    for quote_id in c.completeQuotes:
        if wd_id == quote_id.split("_")[0]:
            quotesById.append(c.completeQuotes[quote_id])
    if printout:
        for completeQuote in quotesById:
            print([quote.quote for quote in list(completeQuote.quotes.values())[0]])
            print("###\n")
        return quotesById
    else:
        return quotesById
