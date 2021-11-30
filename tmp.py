from model.entity_quotes import *
import pickle 
import os

subdir = "/home/kuculo/quotekg/v1_final/en"
forbidden = ["filmography","filmografia",\
"notes","note","примечания","бележки","примітки","ծանոթագրություններ",\
"footnote","각주","зноскі"\
"sources","resources","աղբյուրներ","viri","lähteet","منابع","מקורות",\
"other projects", "altri progetti","iné projekty",\
"external links","weblinks","eksterne henvisninger", "vanjske poveznice", "ссылки","спасылкі", "εξωτερικοί σύνδεσμοι","välislingid","nuorodos","kanpo loturak","külső hivatkozások","eksterne lenker",\
"links","legături externe","lidhje të jashtme","tenglar","externí odkazy","الوصلات الخارجية","پیوند به‌بیرون","קישורים חיצוניים","外部链接","外部リンク","बाहरी कडियाँ",\
"வெளி இணைப்புகள்","Liên kết ngoài","pranala luar","спасылкі","enllaços externs",\
"see also","véase también", "см. также","zobacz też","shiko edhe","რესურსები ინტერნეტში","ראו גם","see","参见",\
"bibliography","bibliografia","kaynakça",\
"related items","voci correlate",\
"works",\
"references","referencias","referencoj","istinadlar", "notennoù","referències","referanser","referime","referencie","sklici","حوالہ جات","参考文献", "சான்றுகள்","మూలాలు","daveoù"\
"literature", "литература", "література"\
]
"""
for root,dirs,files in os.walk(subdir):
    for j, filename in enumerate(files):
        print("%d of %d"%(j, len(files)))
        with open(subdir+"/"+filename,"rb") as f:
            entity=pickle.load(f)
            id = filename[:-4]
            new = EntityWithQuotes(entity,id,"en")
            quotes = list(new.quotes.values())
            t1 = [quote.section_titles for quote in quotes]
            titles = list(set([title for x in t1 for title in x]))
            if "external links" in titles or "External links" in titles:
                print(filename)
                break
"""
f  = open("/home/kuculo/quotekg/v1_final/en/Q450529.pkl", "rb")
entity = pickle.load(f)
section = entity.main_section
language = "en"
b = False
def Q(section):      
    def getQ(section):
        nonlocal quotes
        nonlocal n
        nonlocal level
        nonlocal section_titles
        section_titles = section_titles[:level]
        section_titles.append(section.title.text)
        for line in section.lines:
            n+=1
            quote = untemplatedQuote(section_titles, line, "Q450529", n, language)
            quotes.update({quote.id:quote})
        subsectitles = [sec.title.text for sec in section.sub_sections]
        for sec in section.sub_sections:
            sectitle = sec.title.text
            if sec.title.text.lower() in forbidden:
                continue
            level=level+1
            getQ(sec)
        level=level-1  
        temp_quotes = dict(quotes)
        for quote_id in temp_quotes:
            if not quotes[quote_id]:
                del quotes[quote_id]

    quotes = {}
    n = 1
    level = 0
    section_titles = []
    getQ(section)
    return quotes

quotes = Q(section)
