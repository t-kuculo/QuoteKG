
import os
import pickle
from main import *
ep = "/home/kuculo/quotekg/v2_final"
turp = "/home/kuculo/quotekg/v2_final/Q7251.pkl"
sim = 0.8
"""
print("start")
with open(turp, "rb") as f:
    turing = pickle.load(f)
completeEntity = turing
completeEntity = getEmbs(completeEntity)
all = []
for language in completeEntity.entities:
    quotes = list(completeEntity.entities[language][0].quotes.values())
    for quote in quotes:
        all.append(quote)    
embs = get_embeddings(all)
indices = community_detection(embs, threshold = sim, min_community_size=1,init_max_size=len(all))
new_indices = indices
# split up bias towards same language
for g, quote_cluster in enumerate(indices):
    temp = []
    if len(quote_cluster)<2:
        continue
    else:
        for idx in quote_cluster:
            temp.append(all[idx].page_language)
        if len(list(set(temp))) == 1:
            new_indices = new_indices[:g] + [[t] for t in new_indices[g]] + new_indices[g+1:]
indices = new_indices
print(indices)

"""
qp2 = "/home/kuculo/quotekg/CompleteQuotes2/0.8"
x = []
subdirs = [x[0] for x in os.walk(qp2)][1:] 
for i, subdir in enumerate(subdirs):
    for root,dirs,files in os.walk(subdir):
        for j, filename in enumerate(files):
            if filename.startswith("Q7251_"):
                with open(subdir+"/"+filename,"rb") as f:
                    x.append(pickle.load(f))
with open("/home/kuculo/quotekg/corpus/corpus_v2.pkl","rb") as f:
    c = pickle.load(f)
x = c.lookUp("Q7251", True)
for completeQuote in x:
    for quotes in list(completeQuote.quotes.values()):
        for quote in quotes:
            if hasattr(quote, "quote"):
                print(quote.quote)
            elif hasattr(quote, "translation"):
                print(quote.translation.text)
    print("##\n\n")
