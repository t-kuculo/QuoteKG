#main_section > lines > line > text
#main_section > lines > line > sub_line > text
#main_section > sub_sections
#main_section > templates > type
#main_section > templates > empty_values
#main_section > templates > values
#main_section > templates > sub_templates
#main_section > title > line > text
from transformers.models.auto import configuration_auto
from model.quote import *
languages_with_templates=["fr","da","nl","be","is","ca","bg","da","ka"]
hybrid_languages = ["uk","ru","sv","et"] + ["ko","fa","cs","fi", "hy"]

forbidden = ["filmography","filmografia",\
"notes","note","примечания","бележки","примітки","ծանոթագրություններ",\
"footnote","각주","зноскі"\
"sources","resources","աղբյուրներ","viri","lähteet","منابع","מקורות",\
"other projects", "altri progetti","iné projekty"\
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
class EntityWithQuotes:
    def __init__(self, entity, id, language):
        def necessaryEvil1(section, id):      
            def getQ(section, id):
                nonlocal quotes
                nonlocal n
                nonlocal level
                nonlocal section_titles
                section_titles = section_titles[:level]
                section_titles.append(section.title.text)
                for line in section.lines:
                    n+=1
                    quote = untemplatedQuote(section_titles, line, id, n, language)
                    quotes.update({quote.id:quote})
                for sec in section.sub_sections:
                    if sec.title.text.lower() in forbidden:
                        continue
                    level=level+1
                    getQ(sec, id)
                level=level-1  
                temp_quotes = dict(quotes)
                for quote_id in temp_quotes:
                    if not quotes[quote_id]:
                        del quotes[quote_id]

            quotes = {}
            n = 1
            level = 0
            section_titles = []
            getQ(section, id)
            return quotes

        def necessaryEvil2(section, id):
            def getTempQ(section,  id):
                nonlocal quotes
                nonlocal n
                nonlocal level
                nonlocal section_titles
                section_titles = section_titles[:level]
                section_titles.append(section.title.text)
                for template in section.templates:
                    n+=1
                    templ = template.values
                    quote = templatedQuote(id, n, language, section_titles, **templ)
                    quotes.update({quote.id:quote})
                for sec in section.sub_sections:
                    if sec.title.text.lower() in forbidden:
                        continue
                    level=level+1
                    getTempQ(sec, id)
                level=level-1  
                # filtering for empty Quotes using __bool__
                temp_quotes = dict(quotes)
                for quote_id in temp_quotes:
                    if not quotes[quote_id]:
                        del quotes[quote_id]

            quotes = {}
            n = 1
            level = 0
            section_titles = []
            getTempQ(section, id)
            return quotes


        self.lang=language
        self.entity = entity
        self.id = id
        self.quotes = dict()
        n = 0
        if self.lang in languages_with_templates:
            self.quotes = necessaryEvil2(entity.main_section, id)
        elif self.lang in hybrid_languages:
            self.quotes = necessaryEvil2(entity.main_section, id) 
            self.quotes.update(necessaryEvil1(entity.main_section, self.id))
        else:
            self.quotes = necessaryEvil1(entity.main_section, self.id)

class CompleteEntity():
    def __init__(self, id, entities):
        self.entities = entities
        self.wikiquoteIds = dict()
        self.wikiquotePageIds= dict()
        self.wikipediaIds= dict()
        for language in self.entities:
            self.wikiquoteIds.update({language:self.entities[language][0].entity.wikiquote_id})
            self.wikiquotePageIds.update({language:self.entities[language][0].entity.wikiquote_page_id})
            self.wikipediaIds.update({language:self.entities[language][0].entity.wikipedia_id})
        self.wikidata_id = id


"""
main_section can have lines and/or sub_sections, sub_sections can again have lines and/or subsections
once the first lines are found every other deeper line is just context information
i want to go deeper and deeper until i find a list of lines that is not empty, once i find this
i iterate through the list collecting text. this will be my quote_text (a list)
after this is done, I collect title of every sub_section on way to lines, and under it, and all lines 

entity.main_section.lines = [Line, Line, Line]
entity.main_section.lines[i].text = quote 

>>> e0.main_section.sub_sections[0].lines
[<model.line.Line object at 0x7f315f8afc40>]
>>> e0.main_section.sub_sections[0].sub_sections
[]
>>> e0.main_section.sub_sections[0].title
<model.line.Line object at 0x7f315f8afca0>
>>> e0.main_section.sub_sections[0].title.text
'Nenaveden izvor'
>>> e0.main_section.sub_sections[0].lines[0].text
'"Razuman i pravdoljubiv čovjek od sebe najprije počinje: sebe ispituje i smatra, sebe sudi i osuđuje, niti sebi prašta ako u čemu krivo ima."'


Section
Title: author
    Section
    Title: source named > meta | if sorce not named avoid?
        Line: quote
            link:
            link:
            link:
            line: meta
                footnote: meta
                external link:
"""
"""
section
title: author
    section
    title: quotes from literary works
        line
            line
        line
        line
"""