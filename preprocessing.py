import json
import pickle
from collections import Counter
import os
from model import *
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
model = SentenceTransformer('LaBSE')

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def parseLink(json_link_obj):
    link = Link(json_link_obj["text"], json_link_obj["wikiquoteId"])

    if "prefix" in json_link_obj:
        link.prefix = json_link_obj["prefix"]
    if "wikidataId" in json_link_obj:
        link.wikidata_id = json_link_obj["wikidataId"]
    if "wikipediaId" in json_link_obj:
        link.wikipedia_id = json_link_obj["wikipediaId"]
    if "types" in json_link_obj:
        link.types = json_link_obj["types"]

    return link


def parseTemplate(json_template_obj):
    template = Template(json_template_obj["type"])

    if "emptyValues" in json_template_obj:
        template.empty_values = json_template_obj["emptyValues"]

    if "values" in json_template_obj:
        for key, template_json_obj in json_template_obj["values"].items():
            template.values[key] = parseLine(template_json_obj)

    if "templateValues" in json_template_obj:
        for key, template_json_obj in json_template_obj["templateValues"].items():
            template.sub_templates[key] = parseTemplate(template_json_obj)

    return template


def parseExternalLink(json_external_link_obj):
    external_link = ExternalLink(json_external_link_obj["link"])

    if "text" in json_external_link_obj:
        external_link.text = json_external_link_obj["text"]

    return external_link


def parseLine(json_line_obj):
    line = Line()

    if "text" in json_line_obj:
        line.text = json_line_obj["text"]
        #line.embedding = model.encode(line.text, device='cuda')
    if "bold" in json_line_obj:
        line.bold = json_line_obj["bold"]
    if "italic" in json_line_obj:
        line.italic = json_line_obj["italic"]
    
    if "prefix" in json_line_obj:
        line.prefix = json_line_obj["prefix"]

    if "links" in json_line_obj:
        for json_link_obj in json_line_obj["links"]:
            line.links.append(parseLink(json_link_obj))

    if "footnotes" in json_line_obj:
        for json_footnote_obj in json_line_obj["footnotes"]:
            line.footnotes.append(json_footnote_obj["text"])

    if "externalLinks" in json_line_obj:
        for json_external_link_obj in json_line_obj["externalLinks"]:
            line.external_links.append(parseExternalLink(json_external_link_obj))

    if "templates" in json_line_obj:
        for json_template_obj in json_line_obj["templates"]:
            line.templates.append(parseTemplate(json_template_obj))

    if "subLines" in json_line_obj:
        for json_sub_line_obj in json_line_obj["subLines"]:
            line.sub_lines.append(parseLine(json_sub_line_obj))

    return line


def parseSection(json_section_obj):
    section = Section()

    if "title" in json_section_obj:
        section.title = parseLine(json_section_obj["title"])

    if "chronological" in json_section_obj:
        section.chronological = json_section_obj["chronological"]

    if "templates" in json_section_obj:
        for json_template_obj in json_section_obj["templates"]:
            section.templates.append(parseTemplate(json_template_obj))

    if "lines" in json_section_obj:
        for json_line_pbj in json_section_obj["lines"]:
            section.lines.append(parseLine(json_line_pbj))

    if "sections" in json_section_obj:
        for json_sub_section_pbj in json_section_obj["sections"]:
            section.sub_sections.append(parseSection(json_sub_section_pbj))

    return section


def parseEntity(json_entity_obj):

    entity = Entity(json_entity_obj["wikiquoteId"],json_entity_obj["wikiquotePageId"])

    if "wikidataId" in json_entity_obj:
        entity.wikidata_id = json_entity_obj["wikidataId"]
    if "wikipediaId" in json_entity_obj:
        entity.wikipedia_id = json_entity_obj["wikipediaId"]
    if "types" in json_entity_obj:
        entity.types = json_entity_obj["types"]

    if "sections" in json_entity_obj:
        # there is always 0 or 1 section at the top level
        entity.main_section = parseSection(json_entity_obj["sections"][0])

    return entity

if __name__ == '__main__':
<<<<<<< HEAD
    target_parent_folder= "/home/kuculo/quotekg/v1_final"
    os.mkdir(target_parent_folder)
    for i, filename in enumerate(os.listdir("jsons")): 
        print("%d file of %d"%(i, len(os.listdir("jsons"))))
=======
    target_parent_folder= "/home/kuculo/quotekg/v1"
    os.mkdir(target_parent_folder)
    for i, filename in enumerate(os.listdir("../jsons")): 
        print("%d file of %d"%(i, len(os.listdir("../jsons"))))
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        done=[]
        if filename[8:10] in done or filename[8:11] in done:
                continue
        with open("jsons/"+filename,"r") as file:
            print(filename)
            if filename[8:11]=="sah":
                folder_name = "sah"
                os.mkdir(target_parent_folder+"/"+filename[8:11])
            else:
                folder_name = filename[8:10]
                os.mkdir(target_parent_folder+"/"+folder_name)
            c = Counter()
            for j, line in enumerate(file):
                json_obj = json.loads(line)
                try:
                    entity = parseEntity(json_obj)
                except KeyError:
                    c.update({"-":1})
                    continue
                c.update({"+":1})
                path = target_parent_folder+"/"+folder_name
                if entity.wikidata_id:
                    name = entity.wikidata_id
                else:
                    name = "wq_id_"+str(entity.wikiquote_page_id)
                """
                if isEnglish(entity.wikiquote_id):
                    name = entity.wikiquote_id.replace("/","_")
                else:
                    name = str(entity.wikiquote_page_id)
                """
                with open(path + "/" + name +".pkl" ,"wb") as f:
                    pickle.dump(entity, f)
        with open(path +"/"+"_counter.json","w") as f:
            json.dump(c,f)