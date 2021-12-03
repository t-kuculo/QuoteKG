from model.line import *


class CompleteQuote:   
    def __init__(self, quotes, completeEntity):
        self.quotes = dict()
        self.dates = []
        self.entity = completeEntity
        self.entity.main_section = None # added on 3/12/2021
        self.entity = None # added on 23/11/2021
        #self.entity.entities = None
        self.id = quotes[0].id
        for quote in quotes:
            if quote.language not in self.quotes:
                self.quotes[quote.language] = []
            self.quotes[quote.language].append(quote)
            if hasattr(quote, 'date'):
                self.dates.append(quote.date)
            elif hasattr(quote, 'data'):
                self.dates.append(quote.data)
            