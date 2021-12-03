from main import * 
import pickle
from collections import Counter

from itertools import islice
"""
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


quote_dir = "/home/kuculo/quotekg/completeQuotes2/"
subdirs = [x[0] for x in os.walk(quote_dir)][1:]  
entity_quotes = dict()
entity_quotes["Q937"] = []
entity_quotes["Q15869"] = []
entity_quotes["Q11571"] = []                                                            
for i, subdir in enumerate(subdirs):  
    for root,dirs,files in os.walk(subdir):
        for filename in files:
            if  "Q937_" not in filename and "Q15869_" not in filename and "Q11571_" not in filename:
                continue
            else:
                with open(subdir+"/"+filename,"rb") as f:
                    entity_quotes[filename.split("_")[0]].append(pickle.load(f))

                
our_languages = ["en", "it", "de"]
our_languages.reverse()

corpus_filename = "corpus/corpus_v2.pkl"

print("Load corpus", flush=True)
with open(corpus_filename, "rb") as f:
    corpus = pickle.load(f)

quotes_by_entity = {}
number_of_quote_occurences = 0
number_of_quotes = 0
number_of_entities = 0
number_of_entities_per_language = {}
number_of_quotes_per_language = {}
number_of_quotes_per_entity = {}

for quote_id in corpus.completeQuotes:
    wikidata_id = quote_id.split("_")[0]
    if wikidata_id not in quotes_by_entity:
        quotes_by_entity[wikidata_id] = []
    quotes_by_entity[wikidata_id].append(corpus.completeQuotes[quote_id])

number_of_entities = len(quotes_by_entity.keys())
c2 = Counter()
for entity in quotes_by_entity:
    all_quotes = quotes_by_entity[entity]
    c = Counter()
    for completeQuote in all_quotes:
        number_of_quotes += 1
        if entity not in number_of_quotes_per_entity:
            number_of_quotes_per_entity[entity] = 0
        number_of_quotes_per_entity[entity] += 1
        for lang in completeQuote.quotes:
            if lang not in number_of_quotes_per_language:
                number_of_quotes_per_language[lang] = 0
            number_of_quotes_per_language[lang] += 1
            c.update({lang:len(completeQuote.quotes[lang])})
            number_of_quote_occurences += len(completeQuote.quotes[lang])
            for quote in completeQuote.quotes[lang]:
                c2.update({quote.page_language:1})
    entity_language =c.most_common()[0][0] # Stupid heuristic
    if entity_language not in number_of_entities_per_language:
        number_of_entities_per_language[entity_language] = 0
    number_of_entities_per_language[entity_language] += 1


number_of_entities_per_language = {k: v for k, v in sorted(number_of_entities_per_language.items(), key=lambda item: item[1], reverse = True)}
number_of_quotes_per_language = {k: v for k, v in sorted(number_of_quotes_per_language.items(), key=lambda item: item[1], reverse = True)}
number_of_quotes_per_entity = {k: v for k, v in sorted(number_of_quotes_per_entity.items(), key=lambda item: item[1], reverse = True)}

print("Quote occurences: ", number_of_quote_occurences)
print("Complete Quotes: ", number_of_quotes)
print("Entities: ", number_of_entities)
print("--------------")
print("Entites per languages: ", number_of_entities_per_language)
print("Quotes per language: ", number_of_quotes_per_language)
print("Quotes per entity: ")
for entity in take(15, number_of_quotes_per_entity):
    print(entity, number_of_quotes_per_entity[entity])

Cquotes = quotes_by_entity["Q7251"]
quotes=[]
c = Counter()
for Cquote in Cquotes:
    for lang in Cquote.quotes:
        quotes += Cquote.quotes[lang]

embs = get_embeddings(quotes)
texts = [quote.quote for quote in quotes]
indices = community_detection(embs, threshold = 0.8, min_community_size=1,init_max_size=len(quotes))


for a in indices:
    for i in a:
        print(texts[i])
    print("----")


if len(texts)>2000:
    #changed order of d1/d2
    d1 = texts[:len(texts)//2]
    d2 = texts[len(texts)//2:]                                    
    e1 = model.encode(d1, batch_size=len(d1), show_progress_bar=True)
    e2 = model.encode(d2, batch_size=len(d2), show_progress_bar=True)
    values = numpy.concatenate((e1,e2))
else:
    values = model.encode(texts, batch_size=len(texts), show_progress_bar=True)

new_indices = community_detection(values, threshold = 0.8, min_community_size=1,init_max_size=len(quotes))

for a in new_indices:
    for i in a:
        print(texts[i])
    print("----"),

one = "/home/kuculo/quotekg/CompleteQuotes2/0.8"
two = "/home/kuculo/quotekg/CompleteQuotes/0.8"
x = "/home/kuculo/quotekg/v1_final/"
import os
subdirs = [x[0] for x in os.walk(x)][1:]
e_quotes = {}
for i, subdir in enumerate(subdirs):
    for root, dirs, files in os.walk(subdir):
            for filename in files:
                if "counter" in filename:
                    continue
                id = filename.split("_")[0]
                if id not in e_quotes:
                        e_quotes[id] = []
                path = subdir+"/"+filename
                with open(path, "rb") as f:
                        e_quotes[id].append(pickle.load(f))



#v2_final = 79567 entities
#v2_final total quotes = 672013
# v2_final total quotes per language
c = Counter()
total_count = 0
for entity in e_quotes:
    for language in e_quotes[entity][0].entities:
        quotes = e_quotes[entity][0].entities[language][0].quotes
        total_count += len(quotes)
        c.update({language:len(quotes)})


turing = e_quotes["Q7251.pkl"]
x=[]
for i, e in enumerate(turing):
    x.append(EntityWithQuotes(e, i, "fr"))



"""

x = "/home/kuculo/quotekg/v1_final/"

import os
import pickle
print("all imports done")
subdirs = [x[0] for x in os.walk(x)][1:]
e_quotes = {}
for i, subdir in enumerate(subdirs):
    for root, dirs, files in os.walk(subdir):
            for filename in files:
                if "Q7251" not in filename:
                    continue
                id = filename.split("_")[0]
                if id not in e_quotes:
                        e_quotes[id] = {}
                path = subdir+"/"+filename
                with open(path, "rb") as f:
                        e_quotes[id].update({subdir.split("/")[-1] : pickle.load(f)})
print("e_quotes created")
turing = e_quotes["Q7251.pkl"]
print(turing)
x=dict()
for i, language in enumerate(turing):
    #if language != "fr":
        #continue
    x[language] = EntityWithQuotes(turing[language], str(i), language)

for i in x:
    print(i)
    print(x[i].quotes)
    print("---")

