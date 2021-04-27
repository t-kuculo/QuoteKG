import pickle
import os
import numpy
from collections import Counter
from model.entity_quotes import *
from model.complete_quote import *
from model.utils import *
from itertools import * 
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from model.fast_clustering import community_detection
model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1', device='cuda')
#model.max_seq_length = 512
import json
import gc
gc.collect()
torch.cuda.empty_cache()


def createEntityDicts():
    d ={}
    dir = "/home/kuculo/quotekg/v2_modified"
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
        with open("/home/kuculo/quotekg/v3_modified/"+entity,"wb") as f:
            new = CompleteEntity(entity[:-4], d[entity])
            pickle.dump(new, f) 

def addQuoteAttribute():
    dir = "/home/kuculo/quotekg/v1"
    subdirs = [x[0] for x in os.walk(dir)][1:] 
    print("v2:")                                                                           
    for i, subdir in enumerate(subdirs):
        print("%d of %d complete"%(i, len(subdirs)))  
        language= subdir.split("/")[-1]
        new_dir="/home/kuculo/quotekg/v2_modified/"+language
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
                with open("/home/kuculo/quotekg/v2_modified/"+language+"/"+filename,"wb") as f:
                    id = filename[:-4]
                    new = EntityWithQuotes(entity,id,language)
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
    dir ="/home/kuculo/quotekg/v3_modified/"
    new_dir = "/home/kuculo/quotekg/embeddings/"
    print("Getting encodings")
    files = os.listdir(dir)
    for i, filename in enumerate(files):
        #print(filename)
        print("%d out of %d complete"%(i, len(files)))
        if i<21000:
            continue
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

if __name__ == "__main__":
    addQuoteAttribute()
    createEntityDicts()
    getEmbeddings()
    assignEmbeddings(entity_dir = "/home/kuculo/quotekg/v3_modified/", embedding_dir ="/home/kuculo/quotekg/embeddings/")
    splitEntitiesByLanguage()
    path ="/home/kuculo/quotekg/v4_modified/Q7186.pkl"
    with open(path,"rb") as f:
        e = pickle.load(f)
    evalClustering(e, model, filter=["en","de","it"])

    entity_dir = "/home/kuculo/quotekg/entities_by_language/"
    subdirs = [x[0] for x in os.walk(entity_dir)][1:]  
    for sim in [0.8]:
        if sim !=1:
            counter = Counter()                                                           
            for i, subdir in enumerate(subdirs):  
                print("%d of %d complete"%(i, len(subdirs)))
                for root,dirs,files in os.walk(subdir):
                    for filename in files:
                        with open(subdir+"/"+filename,"rb") as f:
                            completeEntity=pickle.load(f)
                        d = {}
                        all = []
                        for language in completeEntity.entities:
                            quotes = list(completeEntity.entities[language][0].quotes.values())
                            for quote in quotes:
                                all.append(quote)    
                        embs = get_entity_embeddings(all, model)
                        indices = community_detection(embs, threshold = sim, min_community_size=1,init_max_size=len(all))
                        cluster(all, indices, completeEntity)
    #give_context()
    #print("Giving dates")

        give_better_dates_to_completeQuotes(sim, quote_dir = "/home/kuculo/quotekg/darkhorse/0.8")
        create_corpus("/home/kuculo/quotekg/darkhorse2/",0.8)
        convert_to_umbrella_corpus()


