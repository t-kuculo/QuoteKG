from dateparser.search import search_dates
import datetime
import re
from model.my_date_search import DateSearchWithDetection

def my_search_dates(text, language):
    new = []
    if not re.search(r'\d', text):
        return None
    _search_with_detection = DateSearchWithDetection()
    result = _search_with_detection.search_dates(
        text=text, language=language, settings={'RETURN_TIME_AS_PERIOD': True,'REQUIRE_PARTS': ['year']}
    )
    language, dates = result.get('Language'), result.get('Dates')
    if dates:
        for date_tuple in dates:
            period = date_tuple[1].period
            date_obj = date_tuple[1].date_obj
            if period == "day":
                res = (date_obj.year, date_obj.month, date_obj.day)
                return res
                #new.append(res)
            elif period == "month":
                res = (date_obj.year, date_obj.month)
                return res
            elif period == "year":
                res = (date_obj.year)
                return res
    return None
if __name__== "__main__":
    # with period attribute
    dates = my_search_dates("2014 gehe ich nach Hause.", "de")
    if dates:
        for date_tuple in dates:
            period = date_tuple[1].period
            date_obj = date_tuple[1].date_obj
            if period == "day":
                res = (date_obj.year, date_obj.month, date_obj.day)
            elif period == "month":
                res = (date_obj.year, date_obj.month)
            elif period == "year":
                res = (date_obj.year)
            print(res)

    # with period attribute
    dates = my_search_dates("Am 14. März 2014 gehe ich nach Hause.", "de")
    if dates:
        for date_tuple in dates:
            period = date_tuple[1].period
            date_obj = date_tuple[1].date_obj
            if period == "day":
                res = (date_obj.year, date_obj.month, date_obj.day)
            elif period == "month":
                res = (date_obj.year, date_obj.month)
            elif period == "year":
                res = (date_obj.year)
            print(res)



 

