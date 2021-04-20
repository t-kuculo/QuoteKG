import re
pattern_brackets = re.compile(r'\[[^\]]*\]') # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
pattern_brackets2 = re.compile(r'\([^\)]*\)')

pattern_ref = re.compile(r'<ref[^<]*</ref>')
pattern_ref2 = re.compile(r'<ref>[^<]*$')
pattern_ref3 = re.compile(r'<ref[^>]*/>')
pattern_small = re.compile(r'<small[^<]*</small>')
pattern_small2 = re.compile(r'<small>[^<]*$')
pattern_small3 = re.compile(r'<small[^>]*/>')
pattern_multiple_spaces = re.compile(r' +')

def cleanText(text, isQuote=False):
    # remove everything in []
    text = re.sub(pattern_brackets, "", text)
    
    # remove everything in "()" if it is quote text (not in context)
    if isQuote:
        text = re.sub(pattern_brackets2, "", text)

    # remove everything in "<ref"
    text = re.sub(pattern_ref, "", text)
    text = re.sub(pattern_ref2, "", text)
    text = re.sub(pattern_ref3, "", text)
    # remove everything in "<small"
    text = re.sub(pattern_small, "", text)
    text = re.sub(pattern_small2, "", text)
    text = re.sub(pattern_small3, "", text)
    # remove quotation marks at the start and end
    
    if text.endswith('".'):
        text = text[:-2] + '."'
    if text.endswith('».'):
        text = text[:-2] + '.»'

    text = text.strip('\"')
    text = text.strip('\\"')
    text = text.strip('"-”„«»')
    
    # remove any sequences of spaces
    text = re.sub(pattern_multiple_spaces, ' ', text)
    # strip spaces at begin and end
    text = text.strip()
    
    if text == "{{Citace monografie":
        text = None
    
    return text

untemplated = ["eo","en","de","tr","no","hu","ta","he","pt","pl","cy","it","ar","bs","lt","ku","gl","te","hi","sa","sl","hr","sq","sk","ur","sr","eu","el","vi","uz","es","id","th","az","li","kn","ja","si"]
templated = ["fr","da","nl","be","is","ca","bg","da","ka"] +["zh"]
hybrid = ["uk","ru","sv","et"] + ["ko","fa","cs","fi", "hy"]

forbidden_non_alphanumerics_for_context = ["{","}",">","<","@","+","#","&","˛","ˇ","^","`","˙","´","˝","¸"]
forbidden_non_alphanumerics_for_quotes = forbidden_non_alphanumerics_for_context+["[", "]"]


misattributed = ["misattributed","Nesprávně přisuzováno","disputed",\
"Thënie të atribuara gabimisht","fälschlich zugeschrieben","zweifelhaft"]

about = {"en":"quotes about ","de":"zitate mit bezug auf ","fr":"sur ","it":"citazioni su ", "es":"sobre ","nl":"over ", "pl":"o ",\
"ru":"Об ","pt":"sobre","be":"Выказванні пра ","uk":"Про ","ca":"citacions sobre ","hu":"róla mondták",\
"fi":"sanottua","he":"נאמר עליו","fa":"دربارهٔ او","ko":"관련 어록","tr":"Hakkında","sq":"Thënie për të", "ar" : "اقتباسات عن",\
"ro":"despre ", "cs":"ve výrocích"}

about_list = ["quotes about ", "zitate mit bezug auf ", "Ve výrocích","quotes about ","zitate mit bezug auf ","sur ",\
"citazioni su ", "sobre ","Об ","Выказванні пра ","Про ","citacions sobre ","róla mondták","sanottua","נאמר עליו","دربارهٔ او","관련 어록",\
"Hakkında","Thënie për të", ]


attrDict = {
    "bron" : "source","aangehaald" : "cited","taal" : "language","opmerking" : "comment","tekst" : "quote","vertaling" : "translation",
    "نویسنده" : "author",
    "simple" : "quote",
    "ციტატა" : "quote",
    "original": "original","citation": "translation","précisions": "comment","langue": "language","date":"date","parution":"release","source":"source",

    "1":"quote", # Make it work when there are more numbers!!
    "2":"quote",
    "3":"quote",
    "4":"quote",
    "5":"quote",
    "6":"quote",
    "7":"quote",
    "8":"quote",
    "9":"quote",
    "10":"quote",

    "작성일자":"date","제목":"title","출판사":"publisher","url":"url",
    "překladatelé":"translators",
    "titul":"title","příjmení":"surname","místo":"location","isbn":"isbn","vydavatel":"publisher","jméno":"name","rok":"year", "datum přístupu":"access_date","datum vydání":"release_date","issn":"issn",
    "periodikum":"periodical","měsíc":"month","strany":"page",
    "Цитата":"quote","Автор":"author","Коментар":"comment",
    "Комментарий":"comment","Original":"original",
    "Каментар":"comment","Цытата":"quote","Аўтар":"author","крыніца":"source",
    "Tekijä":"author","Viitattu":"referenced","Osoite":"address","Julkaisu":"publication","Nimeke":"title","Ajankohta":"date",
    "útskýring":"explanation", "language":"language","frummál":"quote",
    "cita":"quote","data":"date","lloc":"location","idioma":"language","notes":"notes",
    "editor":"editor","year":"year","publisher":"publisher","page":"page","title":"title","ISBN":"isbn", 
    "archive-date":"archive_date","accessdate":"access_date","archive-url":"archive_url","title":"title","archive_date":"achive:date","access-date":"access_date"
}           
#from googletrans import Translator
from model.line import *
#translator = Translator()
#from nltk.sentiment import SentimentIntensityAnalyzer   
from sentence_transformers import SentenceTransformer
import langdetect
from langdetect import detect
from dateparser import *
ddp = DateDataParser()


#sia = SentimentIntensityAnalyzer()
def isDate(text):
    X= text.split(" ")
    t = ddp.get_date_tuple(text)
    date = None
    if t.date_obj:
        period = t.period
        if period == "day":
            date = (t.date_obj.year, t.date_obj.month, t.date_obj.day)
        elif period == "month":
            date = (t.date_obj.year, t.date_obj.month)
        elif period == "year":
            date = (t.date_obj.year)
    if any(X):
        date = isDate(" ".join(X[1:]))
    return date

def getDate(section_titles):
    # take the last date 
    # print("TITLES: ", len(section_titles))
    date = None
    for title in section_titles:
        date = isDate(title)
    return date

class Context:
    def __init__(self, sub_line):
        self.text = sub_line.text
        #[s.text if isinstance(s,Line) else s for s in line.sub_lines]
        self.text = cleanText(self.text, isQuote=False)
        if len(self.text) < 6 or any([char for char in self.text if char in forbidden_non_alphanumerics_for_context]):
            self.text = None 
        self.entities = sub_line.links
        self.external_links = sub_line.external_links




class untemplatedQuote:   
    def __init__(self, section_titles, line, id, n, lang):
        self.id = id+"_"+lang+"_"+str(n)
        self.section_titles = section_titles
        self.section_titles = [cleanText(title, isQuote=False) for title in self.section_titles]
        self.entities = line.links
        self.contexts = []
        self.page_language = lang
        for sub_line in line.sub_lines:
            if isinstance(sub_line,Line):
                self.contexts.append(Context(sub_line))
        self.footnotes = [s.text if isinstance(s,Line) else s for s in line.footnotes]
        self.external_links = line.external_links
        self.segment_embeddings=[]
        self.embedding = None
        self.date = None
        #self.date=getDate(self.section_titles)
        self.original = None
        if lang == "de":
            self.quote = line.text.split('" -')[:-1]
            if isinstance(self.quote, list):
                self.quote = "".join(self.quote)
            self.direct_context = line.text.split('" -')[-1]
        else:
            self.quote = line.text
        #if the first subline is in a different language, consider it to be the original quote
        if line.bold == None:
            line.bold = []
        if line.italic == None:
            line.italic = []
        self.quote_segments = [line.text[segment[0]:segment[1]] for segment in line.bold] + [line.text[segment[0]:segment[1]] for segment in line.italic] 
        if self.quote:
            self.quote = cleanText(self.quote, isQuote=True)
            if self.quote:
                if len(self.quote) < 6 or any([char for char in self.quote if char in forbidden_non_alphanumerics_for_quotes]):
                     self.quote=None
        
        if self.quote:
            try:
                self.language=detect(self.quote)
            except langdetect.lang_detect_exception.LangDetectException:
                self.language = None
                pass
            self.okay = True
        else:
            self.language = None
            self.okay = False
        self.misattributed = False
        self.about = False

        if self.language:
            if isinstance(self.language,Line):
                self.language = self.language.text
        for title in self.section_titles:
            for x in about_list:
                if x.lower() in title.lower():
                    self.about = True
            if title.lower() in misattributed:
                self.misattributed = True
            if title.lower() in about_list:
                self.about = True

        #if self.quote_segments:
            #self.segment_embeddings = [model.encode(segment, device='cuda') for segment in self.quote_segments]
        #else:
            #self.embedding = model.encode(self.quote, device='cuda')
        #self.language = (translator.detect(self.quote).lang, translator.detect(self.quote).confidence)
        #translation = translator.translate(self.quote)
        #self.sentiment = sia.polarity_scores(translation.text)
        
    def __bool__(self):
        return self.okay and not self.about



class templatedQuote():
    def __init__(self, *args, **kwargs):
        self.direct_context = None
        self.quote_segments = None
        self.section_titles = args[3]
        self.section_titles = [cleanText(title, isQuote=False) for title in self.section_titles]
        self.sentiment = None
        self.date = None
        self.language = None
        self.page_language = args[2]
        self.id = args[0]+"_t_"+args[2]+"_"+str(args[1])
        for key in kwargs:
            if key.lower() in attrDict:
                setattr(self, attrDict[key.lower()], kwargs[key])
        try:
            self.quote = self.quote.text
            self.quote = cleanText(self.quote, isQuote=True)
            if self.quote:
                if len(self.text) < 6 or any([char for char in self.quote if char in forbidden_non_alphanumerics_for_quotes]):
                     self.quote=None
            if not self.language:
                try:
                    self.language=detect(self.quote)
                except langdetect.lang_detect_exception.LangDetectException:
                    self.language = None
                    pass
            self.embedding = None #model.encode(self.quote, device='cuda')
            #if not self.date:
                #self.date=getDate(self.section_titles)
            #sia = SentimentIntensityAnalyzer()
            #self.language = (translator.detect(self.quote).lang, translator.detect(self.quote).confidence)
            #translation = translator.translate(self.quote)
            #self.sentiment = sia.polarity_scores(translation.text)
            self.about = False
            self.misattributed = False

            if self.language:
                if isinstance(self.language,Line):
                    self.language = self.language.text
            for title in self.section_titles:
                for x in about_list:
                    if x.lower() in title.lower():
                        self.about = True
                if title.lower() in misattributed:
                    self.misattributed = True
                if title.lower() in about_list:
                    self.about = True

            self.okay = True
        except AttributeError:
            self.okay=False

    def __bool__(self):
        return self.okay and not self.about

            
            
            
            





"""
no template languages:
["eo","en","de","tr","no","hu","ta","he","pt","pl","cy","it","ar","bs","lt","ku","gl","te","hi","sa","sl","hr","sq","sk","ur","sr","eu","el","vi","uz","es","id","th","az","li",kn]
["ja","si"]> mostly no template
full template languages:
["fr","da","nl","be","is","ca","bg","da","ka"]
hybrid:
["uk","ru","sv","et"]
only context template languages:
["ko","fa","cs","fi", "hy"]
["zh"]> mostly no template for lines
?
'ml', 'gu', 'ro', 'sah', 'su', 'la'
????
["nn"] 

# nl, template : "vertaald citaat"
source = "bron"
cited = "aangehaald"
language = "taal"
remark = "opmerking"
quote = "tekst"
# fa
author = "نویسنده"
# si   
quote = "simple"
# ka Template : "Q"
quote = "ციტატა"
# fr, Template: "citation"
quote = "original"
translation = "citation"
context = "précisions"
language = "langue"
# fr, Template: "Réf"
date = "date"
release = "parution"
source = "source"
# da, Template: "citat"
quote = "1"
# ko, Template: "웹 인용"
posting_date = "작성일자"
title =  "제목"
publisher = "출판사"
url = "url"
# ko, Template: "뉴스 인용"
posting_date = "작성일자"
title =  "제목"
publisher = "출판사"
url = "url"
#cs, Template: "Citace monografie"
translators = "překladatelé"
title = "titul"
surname = "příjmení"
location = "místo"
isbn = "isbn"
publisher = "vydavatel"
name = "jméno"
year = "rok"
#cs, Template: "Citace elektronického periodika"
title = "titul"
surname = "příjmení"
access_date = "datum přístupu"
release_date = "datum vydání"
periodical = "periodikum"
name = "jméno"
url = "url"
#cs, Template: "Citace periodika"
issn = "issn"
periodical = "periodikum"
month = "měsíc"
page = "strany"
year = "rok"
#uk, Template: "Q"
quote = "Цитата"
author = "Автор"
comment = "Коментар"
#uk, Template: "q"
quote = "1"
#,Template: Q
quote = "1"
comment = "Комментарий"
original = "Original"
#sv, Template: citat
quote = "1"
quote = "2"
#be, Template : q
comment = "Каментар"
quote = "Цытата"
author = "Аўтар"
#be, Template: "крыніца" (source)
#fi, Template: "Verkkoviite"
author = "Tekijä"
referenced = "Viitattu"
address = "Osoite"
publication = "Julkaisu"
title = "Nimeke"
date = "Ajankohta"
#it, Template: "NDR" , Template: "Int"
context = "1" # on Line level
#is, Template: Tilvitnun Q30875
quote = "1"
explanation = "útskýring"
language = "language"
original = "frummál"
#ca, Template: "Cita"
quote = "cita"
original = "original"
date = "data"
location = "lloc"
language = "idioma"
notes = "notes"
#bg, Template: "Цитат"
quote = "1" #and other numbers of course
#et, Template: "halliga"
quote = "1"
#ja, Template: "lang"??
#hy, Template: "cite book"
editor = "editor"
year = "year"
publisher = "publisher"
page = "page"
title = "title"
ISBN = "ISBN"
#zh, Template: "cite web"
archive_date = "archive-date"
accessDate = "accessdate"
archive_url = "archive-url"
title = "title"
url = "url"
#zh, Template: "cite news"
archive_date = "archive-date"
accessDate = "access-date"
archive_url = "archive-url"
title = "title"
url = "url"
#zh: lines starting with  "原文:" (original)
#zh, Template:"lang" under a line
"""