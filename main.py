import pickle
import os
import numpy
import collections
import configparser
from model.entity_quotes import *
from model.complete_quote import *
from model.utils import *
from itertools import * 
from pathlib import Path
from sentence_transformers import SentenceTransformer, models
from scipy.spatial import distance
from model.fast_clustering import community_detection
import multiprocessing
import math
from transformers import pipeline
import json
import gc
import json
#model.max_seq_length = 512

gc.collect()
torch.cuda.empty_cache()


def getEmbs(completeEntity):
    """
    Maybe make all the dicts ordered?
    """
    quotes = {}
    size = 1024
    # all = []
    all = {}
    texts = []
    remember = []
    for language in completeEntity.entities:
        quotes = list(completeEntity.entities[language][0].quotes.values())
        for quote in quotes:
            all.update({quote.id : quote})
            #all.append(quote) 

    for j, i in enumerate(all.values()):
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

    if all == []:
        print(completeEntity.wikidata_id)
        return completeEntity

    gc.collect()
    torch.cuda.empty_cache()
    with torch.no_grad():
        if len(all)>2000:
            d1 = texts[:len(texts)//2]
            d2 = texts[len(texts)//2:]               
            # Tokenize sentences
            #encoded_input1 = tokenizer(d1, padding=True, truncation=True, return_tensors='pt')
            #encoded_input2 = tokenizer(d2, padding=True, truncation=True, return_tensors='pt')
            # Compute token embeddings
            #with torch.no_grad():
                #model_output = model(**encoded_input1)
            # Perform pooling. In this case, max pooling.
            #e1 = mean_pooling(model_output, encoded_input1['attention_mask'])    
            #e2 = mean_pooling(model_output, encoded_input2['attention_mask'])                          
            e1 = model.encode(d1)
            e2 = model.encode(d2)
            values = numpy.concatenate((e1,e2))
        else:
            #encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
            #with torch.no_grad():
                #model_output = model(**encoded_input)
            #values =  mean_pooling(model_output, encoded_input['attention_mask']) 
            values = model.encode(texts)

    for quote_id, embedding in zip(all, values):
        for language in completeEntity.entities:
            if quote_id not in completeEntity.entities[language][0].quotes:
                continue
            completeEntity.entities[language][0].quotes[quote_id].embedding = embedding

    return completeEntity


def X(subdirs, files, intermediate_done=False):
    d ={}
    print("v2:")  
    if not os.path.isdir(entity_dir):
        os.mkdir(entity_dir)                                                                          
    if not intermediate_done:
        for i, subdir in enumerate(subdirs):
            print(subdir)
            print("%d of %d complete"%(i, len(subdirs)))  
            language= subdir.split("/")[-1]
            new_dir= entity_dir+language
            if not os.path.isdir(new_dir):
                os.mkdir(new_dir)                
            for root,dirs,files in os.walk(subdir):
                for j, filename in enumerate(files):
                    print("%d file out of %d"%(j, len(files)))
                    if "counter" in filename:
                        continue
                    with open(subdir+"/"+filename,"rb") as f:
                        entity=pickle.load(f)
                        id = filename[:-4]
                        new = EntityWithQuotes(entity,id,language)
                        if not os.path.isdir(embedded_quote_files_path):      
                            os.mkdir(embedded_quote_files_path)
                        if not os.path.isdir(embedded_quote_files_path + language):      
                            os.mkdir(embedded_quote_files_path + language)
                        with open(embedded_quote_files_path + language+"/"+filename,"wb") as g:
                            pickle.dump(new, g)

    else:
        s, e = files
        subdirs = [x[0] for x in os.walk(embedded_quote_files_path )][1:] 
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
        od = collections.OrderedDict(sorted(d.items())[s:e])
        d = {}
        for i, filename in enumerate(od):
            print("%d of %d complete"%(i, len(od))) 
            path = entity_dir+filename
            path = Path(path)
            #if path.exists():
                #continue
            print(filename)
            with open(entity_dir+filename,"wb") as f:
                new = CompleteEntity(filename[:-4], od[filename])
                new = getEmbs(new)
                pickle.dump(new, f)
        



if __name__ == "__main__":
    settings.init()
    sim = 0.8
    threads = []
    # Loading paths from config file
    config = configparser.ConfigParser()
    config.read("config.ini")
    processed_files_path = config.get("Paths","processed_files_path")
    entity_dir = config.get("Paths","entity_files_path")
    embedded_quote_files_path = config.get("Paths","embedded_quote_files_path")
    quotes_path = config.get("Paths","clustered_quotes_path")
    improved_clustered_quotes_path = config.get("Paths","improved_clustered_quotes_path")
    corpus_path = config.get("Paths","corpus_path")
    # Loading language subdirectories from config file
    languages = ["L1","L2","L3","L4","L5"]
    all_subdirs = [[processed_files_path + language for language in json.loads(config.get("Defaults",L))] for L in languages]
    # Partitioning work with multiprocessing
    cpt = sum([len(files) for r, d, files in os.walk(embedded_quote_files_path)])
    partitions = math.ceil(cpt/3000)
    all_files = [(i*5000, (i+1)*5000) for i in range(partitions)]
    # Extracting quotes
    X(all_subdirs[0], [], intermediate_done=False)
    """
    for subdirs in all_subdirs:
        t = multiprocessing.Process(target=X,
        args=(
             subdirs,
             [],
             False
        ))
        threads.append(t)
        t.start()
    for t in threads:
            t.join()
    # Embedding quotes
    
    threads = []
    """
    for files in all_files:
        t = multiprocessing.Process(target=X, 
        args=(
            [],
            files,
            True
        ))
        threads.append(t)
        t.start()
    for t in threads:
            t.join()
    
    print("Embeddings created")
    
    # Clustering quotes
    print("Clustering")
    for root,dirs,files in os.walk(entity_dir):
        for z, filename in enumerate(files):
            with open(entity_dir+"/"+filename,"rb") as f:
                try:
                    completeEntity=pickle.load(f)
                except EOFError as error:
                    continue
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
            cluster(all, indices, completeEntity, path=quotes_path)
            print("%d of %d finished clustering"%(z,len(files)))

    #give_context()
    print("Adding context to quotes")
    give_better_dates_to_completeQuotes(quotes_path, improved_clustered_quotes_path)
    print("Creating corpus")
    create_corpus(improved_clustered_quotes_path, corpus_path)
    print("Creating umbrella corpus")
    convert_to_umbrella_corpus(corpus_path)

    


