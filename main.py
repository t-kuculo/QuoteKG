import pickle
import os
import numpy
from collections import Counter
import collections
from model.entity_quotes import *
from model.complete_quote import *
from model.utils import *
from itertools import * 
from pathlib import Path
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from model.fast_clustering import community_detection
model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1', device='cuda')
#model.max_seq_length = 512
import json
import gc
gc.collect()
torch.cuda.empty_cache()
"""
started v1>v2 at 13:24
TODO: v1 > completeQuotes_v4/ (pass entityWithQuotes(v2) directly to CompleteEntity(v3), get embeddings(v4) immediately and save them,
> cluster > create umbrella corpus

"""

def getq(e):
    all = []
    for language in e.entities:
        quotes = list(e.entities[language][0].quotes.values())
        for quote in quotes:
            all.append(quote) 
    return all

def getEmbs(completeEntity):
    """
    Maybe make all the dicts ordered?
    """
    quotes = {}
    embeddings = {} 
    size = 1024
    #quote_batch, n_of_quotes = get_all_entity_quotes(completeEntity)
    all = []
    texts = []
    remember = []
    for language in completeEntity.entities:
        quotes = list(completeEntity.entities[language][0].quotes.values())
        for quote in quotes:
            all.append(quote) 
    for j, i in enumerate(all):
        if hasattr(i, "quote"):
            if hasattr(i.quote, "text"):
                texts.append(i.quote.text)
            else:
                texts.append(i.quote)
        elif hasattr(i, "original"):
            if hasattr(i.original, "text"):
                texts.append(i.original.text)
            else:
                texts.append(i.original)
        elif hasattr(i, "translation"):
            if hasattr(i.translation, "text"):
                texts.append(i.translation.text)
            else:
                texts.append(i.translation)
        else:
            # if we somehow got a quote object without quote, orginal or translation attribute. We want to delete it from the list
            remember.append(j)
            inv_map = {v: k for k, v in completeEntity.entitiesitems()}
            for language in completeEntity.entities:
                if j > len(list(completeEntity.entities[language][0].quotes.values())):
                    j = j - len(list(completeEntity.entities[language][0].quotes.values()))
                else:
                    inv_map = {v: k for k, v in completeEntity.entities[language][0].quotes.items()}
                    key = inv_map[i]
                    del completeEntity.entities[language][0].quotes[key]           
    for index in sorted(remember, reverse=True):
        del all[index]
    #quotes.update(quote_batch)
    #if list(quotes.values()) == []:
    if all == []:
        print(completeEntity.wikidata_id)
        return completeEntity
    gc.collect()
    torch.cuda.empty_cache()
    with torch.no_grad():
        if len(all)>2000:
            #changed order of d1/d2
            d1 = texts[:len(texts)//2]
            d2 = texts[len(texts)//2:]                                 
            e1 = model.encode(d1)
            e2 = model.encode(d2)
            values = numpy.concatenate((e1,e2))
        else:
            values = model.encode(texts)
        n=0
        for language in completeEntity.entities:
            #for quote in list(completeEntity.entities[language][0].quotes.values()):
            for quote_id, value in zip(completeEntity.entities[language][0].quotes, values[n:]):
                completeEntity.entities[language][0].quotes[quote_id].embedding = value
                n+=1
    return completeEntity

def createEntityDicts():
    d ={}
    dir = "/home/kuculo/quotekg/v2"
    subdirs = [x[0] for x in os.walk(dir)][1:]                                                                            
    for subdir in subdirs:  
        language = subdir.split("/")[-1]
        for root,dirs,files in os.walk(subdir):
            for filename in files:
                if "counter" in filename:
                    continue
                if filename not in d:
                    d[filename] = {}
                if language not in d[filename]:
                    d[filename].update({language:[]})
                with open(subdir+"/"+filename,"rb") as f:
                    #print(subdir+"/"+filename)
                    entity=pickle.load(f)
                    d[filename][language].append(entity)
    for entity in d:
        with open("/home/kuculo/quotekg/v3/"+entity,"wb") as f:
            new = CompleteEntity(entity[:-4], d[entity])
            pickle.dump(new, f) 

def addQuoteAttribute():
    dir = "/home/kuculo/quotekg/v1"
    subdirs = [x[0] for x in os.walk(dir)][1:] 
    print("v2:")  
    if not os.path.isdir("/home/kuculo/quotekg/v2"):
        os.mkdir("/home/kuculo/quotekg/v2")
                                                                                 
    for i, subdir in enumerate(subdirs):
        print("%d of %d complete"%(i, len(subdirs)))  
        language= subdir.split("/")[-1]
        new_dir="/home/kuculo/quotekg/v2/"+language
        if os.path.isdir(new_dir):
            continue
        else:
            os.mkdir(new_dir)
        for root,dirs,files in os.walk(subdir):
            for j, filename in enumerate(files):
                #print("%d of %d complete"%(j, len(files))) 
                if "counter" in filename:
                    continue
                #print(subdir)
                #print(filename)
                with open(subdir+"/"+filename,"rb") as f:
                    entity=pickle.load(f)
                with open("/home/kuculo/quotekg/v2/"+language+"/"+filename,"wb") as f:
                    id = filename[:-4]
                    new = EntityWithQuotes(entity,id,language)
                    pickle.dump(new, f)
"""
subdir = "/home/kuculo/quotekg/v1_final/en"
some = []
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
                break
"""
def X(intermediate_done=False):
    d ={}
    dir = "/home/kuculo/quotekg/v1_final"
    subdirs = [x[0] for x in os.walk(dir)][1:] 
    subdirs = ["/home/kuculo/quotekg/v1_final/it", "/home/kuculo/quotekg/v1_final/en"]
    print("v2:")  
    if not os.path.isdir("/home/kuculo/quotekg/v2_final"):
        os.mkdir("/home/kuculo/quotekg/v2_final")                                                                          
    if not intermediate_done:
        for i, subdir in enumerate(subdirs):
            print(subdir)
            print("%d of %d complete"%(i, len(subdirs)))  
            language= subdir.split("/")[-1]
            new_dir="/home/kuculo/quotekg/v2_final/"+language
            if os.path.isdir(new_dir):
                continue
            else:
                os.mkdir(new_dir)
            for root,dirs,files in os.walk(subdir):
                for j, filename in enumerate(files):
                    if j%100==0:
                        print("%d file out of %d"%(j, len(files)))
                    if "counter" in filename:
                        continue
                    with open(subdir+"/"+filename,"rb") as f:
                        entity=pickle.load(f)
                        id = filename[:-4]
                        new = EntityWithQuotes(entity,id,language)
                        if not os.path.isdir("/home/kuculo/quotekg/intermediate/"+ language):      
                            os.mkdir("/home/kuculo/quotekg/intermediate/"+ language)
                        with open("/home/kuculo/quotekg/intermediate/"+ language+"/"+filename,"wb") as g:
                            pickle.dump(new, g)
                        if filename not in d:
                            d[filename] = {}
                        if language not in d[filename]:
                            d[filename].update({language:[]})
                            d[filename][language].append(new)
    else:
        subdirs = [x[0] for x in os.walk("/home/kuculo/quotekg/intermediate/")][1:] 
        for i, subdir in enumerate(subdirs):
            language = subdir.split("/")[-1]
            for root,dirs,files in os.walk(subdir):
                for j, filename in enumerate(files):
                    if j%100==0:
                        print("%d file out of %d"%(j, len(files)))
                    if "counter" in filename:
                        continue
                    with open(subdir+"/"+filename,"rb") as f:
                        entity=pickle.load(f)
                        if filename not in d:
                            d[filename] = {}
                        if language not in d[filename]:
                            d[filename].update({language:[]})
                            d[filename][language].append(entity)
    print("Creating CompleteEntities and embedding quotes")
    #multiprocessing
    # od = collections.OrderedDict(sorted(d.items())[:5000])
    od = collections.OrderedDict(sorted(d.items())[25000:30000])
    # od = collections.OrderedDict(sorted(d.items())[50000:55000])
    d = None
    for i, filename in enumerate(od):
        print("%d of %d complete"%(i, len(od))) 
        path = "/home/kuculo/quotekg/v2_final/"+filename
        path = Path(path)
        if path.exists():
            continue
        print(filename)
        with open("/home/kuculo/quotekg/v2_final/"+filename,"wb") as f:
            new = CompleteEntity(filename[:-4], od[filename])
            new = getEmbs(new)
            pickle.dump(new, f)
      
def clusterEmbeddings(completeEntity):
    entities = completeEntity.entities
    X = {}
    for l1, l2 in combinations(entities, 2):
        e1 = entities[l1][0]
        e2 = entities[l2][0]
        quotes1, quotes2 = e1.quotes, e2.quotes
        for quote1, quote2 in list(product(quotes1,quotes2)):
            if quote1.id not in X and quote2.id not in X:
                X[quote1.id].update({l1:quote1})
            embeddings = model.encode([quote1.quote, quote2.quote])
            similarity = 1 - distance.cosine(embeddings[0],embeddings[1])
            if similarity > 0.5:
                X[quote1.id][l2]=quote2
            else:
                X[quote2.id].update({l2:quote2})
    return

def getEmbeddings():
    quotes = {}
    embeddings = {} 
    dir ="/home/kuculo/quotekg/v3/"
    new_dir = "/home/kuculo/quotekg/embeddings/"
    print("Getting encodings")
    files = os.listdir(dir)
    for i, filename in enumerate(files):
        #print(filename)
        print("%d out of %d complete"%(i, len(files)))
        #if i<21000:
            #continue
        with open(dir+"/"+filename,"rb") as f:
            entity=pickle.load(f)
        size = 1024
        quotes.update(get_all_entity_quotes(entity))
        gc.collect()
        torch.cuda.empty_cache()
        if len(quotes.keys())>size:
            with torch.no_grad():
                if len(quotes)>2000:
                    d1 = dict(list(quotes.items())[len(quotes)//2:])
                    d2 = dict(list(quotes.items())[:len(quotes)//2])                   
                    #print(values)  
                    #print(len(values))                 
                    e1 = model.encode(list(d1.values()), batch_size=len(d1.keys()), show_progress_bar=True)
                    e2 = model.encode(list(d2.values()), batch_size=len(d2.keys()), show_progress_bar=True)
                    values = numpy.concatenate((e1,e2))
                else:
                    values = model.encode(list(quotes.values()), batch_size=len(quotes.keys()), show_progress_bar=True)
            for key,value in zip(quotes, values):
                with open(new_dir+key+".pkl","wb") as f:
                    pickle.dump(value, f)
            
            quotes = {}
    values = model.encode(list(quotes.values()), batch_size=len(quotes.keys()), show_progress_bar=True)
    for key,value in zip(quotes, values):
                with open(new_dir+key+".pkl","wb") as f:
                    pickle.dump(value, f)

def smallTest():
    dir = "/home/kuculo/quotekg/v1"
    subdirs = [x[0] for x in os.walk(dir)][1:]                                                                          
    for i, subdir in enumerate(subdirs):
        language= subdir.split("/")[-1]
        for root,dirs,files in os.walk(subdir):
            for filename in files:
                #if "Q16721538" not in filename:
                if "Q3836804" not in filename:
                    continue
                with open(subdir+"/"+filename,"rb") as f:
                    entity=pickle.load(f)
                id = filename[:-4]
                new = EntityWithQuotes(entity,id,language)
                #new.entity.print()
                print("$$$$")
                print(new.quotes)
                for quote in new.quotes.values():
                    print(quote.quote)
                    print(quote.embedding)

def smallTest2():
    with open("/home/kuculo/quotekg/v4/Q3836804.pkl","rb") as f:
        entity=pickle.load(f)
    print("$$$$")
    print(entity.entities)
    for language in entity.entities:
        for quote in language[0].quotes.values():
            print(quote.quote) 
            print(quote.embedding)

if __name__ == "__main__":
    X(intermediate_done=True)
    while(True):
        print("embedding completed")
    entity_dir = "/home/kuculo/quotekg/v2_final/"
    #subdirs = [x[0] for x in os.walk(entity_dir)][1:]  
    sim = 0.8
    print("Embeddings created")
    print("Clustering")
    for root,dirs,files in os.walk(entity_dir):
        for z, filename in enumerate(files):
            with open(entity_dir+"/"+filename,"rb") as f:
                completeEntity=pickle.load(f)
            all = []
            for language in completeEntity.entities:
                quotes = list(completeEntity.entities[language][0].quotes.values())
                for quote in quotes:
                    all.append(quote)    
            embs = get_embeddings(all)
            indices = community_detection(embs, threshold = sim, min_community_size=1,init_max_size=len(all))
            new_indices = indices
            # split up bias towards same language
            for g, cluster in enumerate(indices):
                temp = []
                if len(cluster)<2:
                    continue
                else:
                    for i in cluster:
                        temp.append(i.page_language)
                    if len(list(set(temp))) == 1:
                        new_indices = new_indices[:g] + [[t] for t in new_indices[g]] + new_indices[g+1:]
            indices = new_indices
            cluster(all, indices, completeEntity, path="/home/kuculo/quotekg/CompleteQuotes/"+str(sim))
            print("%d of %d finished clustering"%(z,len(files)))
    
    #give_context()
    print("Starting better dates")
    give_better_dates_to_completeQuotes(sim, quote_dir = "/home/kuculo/quotekg/CompleteQuotes/"+str(sim))
    print("Creating corpus")
    create_corpus("/home/kuculo/quotekg/CompleteQuotes2/"+str(sim))
    print("Creating umbrella corpus")
    convert_to_umbrella_corpus()


