import os
import os.path
import pickle
from model.fast_clustering import *
from model.complete_quote import *
from model.corpus import *
from model.umbrella import *
from itertools import *
from sentence_transformers.util import *
from sklearn.neighbors import BallTree
import networkx 
from networkx.algorithms.components.connected import connected_components
from model.date_parsing_with_period import * 
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from model.fast_clustering import community_detection
import numpy
import gc


def recluster():
    with open("/home/kuculo/quotekg/corpus/corpus_v2.pkl", "rb") as f:
        corpus = pickle.load(f)
    ids = sorted(corpus.all_ids)
    texts = []
    for z, id in enumerate(ids):
        if z%1000==0:
            print("%d out of %d done reclustering"%(z, len(ids)))
        quotes = lookUp(corpus, id)
        for quote in quotes:
            if hasattr(quote, "quote"):
                if hasattr(quote.quote, "text"):
                    texts.append(quote.quote.text)
                else:
                    texts.append(quote.quote)
            elif hasattr(quote, "original"):
                if hasattr(quote.original, "text"):
                    texts.append(quote.original.text)
                else:
                    texts.append(quote.original)
            elif hasattr(quote, "translation"):
                if hasattr(quote.translation, "text"):
                    texts.append(quote.translation.text)
                else:
                    texts.append(quote.translation)
        gc.collect()
        torch.cuda.empty_cache()
        with torch.no_grad():
            if len(texts)>2000:                            
                e1 = model.encode(texts[:len(texts)//2])
                e2 = model.encode(texts[len(texts)//2:] )
                values = numpy.concatenate((e1,e2))
            else:
                values = model.encode(texts)
                    
        indices = community_detection(values, threshold = 0.8, min_community_size=1,init_max_size=len(texts))
        new_indices = indices
        # split up bias towards same language
        for g, quote_cluster in enumerate(indices):
            temp = []
            if len(quote_cluster)<2:
                continue
            else:
                for idx in quote_cluster:
                    temp.append(quotes[idx].page_language)
                if len(list(set(temp))) == 1:
                    new_indices = new_indices[:g] + [[t] for t in new_indices[g]] + new_indices[g+1:]
        indices = new_indices
        for index_cluster in indices:
            tmp = []
            for idx in index_cluster:
                tmp.append(quotes[idx])
            corpus.completeQuotes[id] = CompleteQuote(tmp)
    with open("/home/kuculo/quotekg/corpus/final.pkl", "wb") as f:
        pickle.dump(corpus, f)


def cluster(quotes, indices, completeEntity, path):
    for cluster in indices:
        quote_cluster = []
        for index in cluster:
            quote_cluster.append(quotes[index])
        n = len(quote_cluster)
        new_path = path+"/"+str(n)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        rep_id = quote_cluster[0].id
        completeQuote = CompleteQuote(quote_cluster, completeEntity)
        new_folder_path = new_path+"/"
        with open(new_folder_path+rep_id+".pkl","wb") as f:
            pickle.dump(completeQuote, f)

def get_entity_embeddings(all, model):
    return[model.encode(quote.quote) for quote in all]

def get_embeddings(all):
    return[quote.embedding for quote in all]

def to_graph(l):
    G = networkx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G

def to_edges(l):
    """ 
        treat `l` as a Graph and returns it's edges 
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current               

def get_all_entity_quotes(entity):
    batch_of_quotes = {}
    n_of_quotes = []
    entities = entity.entities
    for language in entities:
        entity = entities[language][0]
        quotes = entity.quotes
        n_of_quotes.append(len(list(quotes.values())))
        for quote in list(quotes.values()):
            if quote:
                if quote.id in batch_of_quotes:
                    print("Quote IDs don't work! You have duplicates!")
                    return
                else:
                    batch_of_quotes[quote.id] = ''
                if quote.quote_segments:
                    for segment in quote.quote_segments:
                        batch_of_quotes[quote.id]+=segment.lower()
                else:
                    batch_of_quotes[quote.id]=quote.quote.lower()
    return batch_of_quotes, n_of_quotes



def checkQuotes(completeEntity, counter):
    entities = completeEntity.entities
    for lang in entities:
        entity = entities[lang][0]
        quotes = entity.quotes
        if not quotes:
            #print(lang)
            counter.update({lang:1})
            entity.entity.print()
            #print()
    return counter

def assignEmbeddings(entity_dir, embedding_dir):
    print("Assigning embeddings:")
    for (root,dirs,files) in os.walk(entity_dir):
        for filename in files:
            #print("%d out of %d assigned"%(i, len(files)))
            print(filename)
            with open(entity_dir+filename,"rb") as f:
                complete_entity=pickle.load(f)
            entities = complete_entity.entities
            for language in entities:
                entity = entities[language][0]
                quotes = entity.quotes
                for quote_id in quotes:
                    file = embedding_dir+quote_id+".pkl"
                    if os.path.isfile(file):
                        with open(file,"rb") as f:
                            quotes[quote_id].embedding = pickle.load(f)
                    else:
                        print("file not found: ",file)
                        continue
            with open("/home/kuculo/quotekg/v4_modified/"+filename,"wb") as f:
                pickle.dump(complete_entity, f) 
                            
def matchEntityQuotes_simpleClustering(file_path):
    all_quotes = dict()
    with open(file_path,"rb") as f:
        completeEntity=pickle.load(f)
    entities = completeEntity.entities
    n = len(list(entities.keys()))
    X = []
    Y = []
    print("now")
    for language in entities:
        all_quotes.update(entities[language][0].quotes)
        Y.append(list(entities[language][0].quotes.values()))

    for language_cluster in Y:
        X.append([])
        for quote in language_cluster:
            X[-1].append(quote.embedding)

    quotes = [quote for quote in all_quotes.values()]
    embeddings = [quote.embedding for quote in all_quotes.values()] 

    clusters = community_detection(embeddings, threshold = 0.9, min_community_size=1, init_max_size=n)
    final_quotes = []
    for cluster in clusters:
            temp = []
            for index in cluster:
                quote = quotes[index]
                temp.append(quote)
            completeQuote = CompleteQuote(temp)
            rep_id = temp[0].id
            new_folder_path = "/home/kuculo/quotekg/completeQuotes/"+str(n)+"/"
            with open(new_folder_path+rep_id+".pkl","wb") as f:
               pickle.dump(completeQuote, f)

def my_distance(emb1, emb2):
    return 1 - float(util.pytorch_cos_sim(emb1, emb2)[0][0])

def compareSublines(quote1, quote2):
    subl1 = quote1.context["sub_lines"]
    subl2 = quote2.context["sub_lines"]
    if subl1 and subl2:
        for line1 in subl1:
            for line2 in subl2:
                #embeddings = model.encode([line1, line2])
                #similarity = 1 - distance.cosine(embeddings[0],embeddings[1])
                similarity = 1 - distance.cosine(line1.embedding, line2.embedding)
                if similarity > 0.5:
                    return similarity-0.5
    return 0            

def createQuoteSimilarityScore(completeEntity):
    entities = completeEntity.entities
    index = dict()
    X = {}
    for l1, l2 in combinations(entities, 2):
        e1 = entities[l1][0]
        e2 = entities[l2][0]
        quotes1, quotes2 = e1.quotes, e2.quotes
        for i, quotes in enumerate(list(product(quotes1,quotes2))):
            quote1, quote2 = quotes
            #print("%d out of %d"%(i,len(quotes1)+ len(quotes2)))
            #if quote1.id not in X and quote2.id not in X:
            if quote1 not in X:
                #X[quote1.id].update({l1:quote1})
                X[quote1] = {}
                X[quote1].update({l1:quote1})
            #embeddings = model.encode([quote1.quote, quote2.quote])
            #similarity = 1 - distance.cosine(embeddings[0],embeddings[1])
            similarity = 1 - distance.cosine(quote1.quote.embedding, quote2.quote.embedding)
            alpha = compareSublines(quote1, quote2)
            if similarity+alpha > 0.9:
                #X[quote1.id].update({l2:quote2})
                X[quote1].update({l2:quote2})
                if quote1 not in index:
                    index[quote1] = []
                index[quote1].append(quote2)
                if quote2 not in index:
                    index[quote2] =  []
                index[quote2].append(quote1)
            else:
                X[quote2] = {}
                X[quote2].update({l2:quote2})
                #X[quote2.id].update({l2:quote2})
    return X, index 

def getDates(completeQuote):
    dates = []
    new_quotes = dict()
    for language in completeQuote.quotes:
        if language not in new_quotes:
            new_quotes[language] = []
        temp = []
        language_cluster = completeQuote.quotes[language]
        for quote in language_cluster:
            section_titles = quote.section_titles  
            page_language = quote.page_language
            date1 = getDate(section_titles,page_language)
            if hasattr(quote, "quote"):
                date2 = getDateFromContext(quote.quote)
            elif hasattr(quote,"translation"):
                date2 = getDateFromContext(quote.translation)
            elif hasattr(quote, "original"):
                date2 = getDateFromContext(quote.original)
            if date1 and date2:
                if len(date1) == len(date2):
                    quote.date = date1
                else:
                    quote.date = max([date1,date2], key=lambda x: len(x))
            elif date1:
                quote.date = date1
            else:
                quote.date = date2
            new_quotes[language].append(quote)
            temp.append(quote.date)
        dates.append(temp)
    return dates, new_quotes

def getDate(section_titles, language):
    # take the last date 
    date = None
    for title in section_titles:
        date = my_search_dates(title, language)
    return date

def getDateFromContext(quote):
    if hasattr(quote, "contexts"):
        contexts = [context.text for context in quote.contexts]
        for context in contexts:
            date=getDate(contexts, quote.page_language)
            if date:
                return date

def give_better_dates_to_completeQuotes(threshold, quote_dir="/home/kuculo/quotekg/CompleteQuotes/0.8"):
    print("hello")
    subdirs = [x[0] for x in os.walk(quote_dir)][1:]    
    print(subdirs)                                                  
    for i, subdir in enumerate(subdirs): 
        sub = subdir.split("/")[-1] 
        print("%d folder  out of %d"%(i, len(subdirs)))
        for root,dirs,files in os.walk(subdir):
            for j, filename in enumerate(files):
                print("%d file  out of %d"%(j, len(files)))
                with open(subdir+"/"+filename,"rb") as f:
                    completeQuote = pickle.load(f)
                    completeQuote.dates, completeQuote.quotes = getDates(completeQuote)
                    completeQuote.entity = None
                new_quote_dir = "/home/kuculo/quotekg/CompleteQuotes2/0.8"
                new_path = new_quote_dir+"/"+subdir.split("/")[-1]
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                with open(new_path+"/"+filename,"wb") as f:
                    pickle.dump(completeQuote, f)

def get_context(completeQuote):
    new_quotes=dict()
    id = completeQuote.id
    with open("/home/kuculo/quotekg/completeQuotes_v3/"+id+".pkl", "rb") as f:
        newCompleteQuote=pickle.load(f)
    completeQuote.entity = newCompleteQuote.entity
    for language in completeQuote.quotes:
        new_quotes[language] = []
        quotes = completeQuote.quotes[language]
        for quote in quotes:
            quote_id = quote.id
            date = quote.date
            embedding = quote.embedding
            new_quote = completeQuote.entity.quotes[quote_id]
            new_quote.date = date
            new_quote.embedding = embedding
            new_quotes[language].append(new_quote)
    completeQuote.quotes = new_quotes
    return completeQuote

def give_context():
    quote_dir = "/home/kuculo/quotekg/completeQuotes_with_dates/"
    subdirs = [x[0] for x in os.walk(quote_dir)][1:]                                                         
    for i, subdir in enumerate(subdirs): 
        sub = subdir.split("/")[-1] 
        print("%d folder  out of %d"%(i, len(subdirs)))
        for root,dirs,files in os.walk(subdir):
            for j, filename in enumerate(files):
                print("%d file  out of %d"%(j, len(files)))
                with open(subdir+"/"+filename,"rb") as f:
                    completeQuote = pickle.load(f)
                    completeQuote = get_context(completeQuote)
                if not os.path.isdir("/home/kuculo/quotekg/v5/"+sub):
                    os.mkdir("/home/kuculo/quotekg/v5/"+sub)
                with open("/home/kuculo/quotekg/v5/"+sub+"/"+filename,"wb") as f:
                    pickle.dump(completeQuote, f)

def create_corpus(quote_dir):
    print("creating corpus")
    quotes = set()
    subdirs = [x[0] for x in os.walk(quote_dir+"/")][1:]    
    for i, subdir in enumerate(subdirs): 
        sub = subdir.split("/")[-1] 
        print("%d folder  out of %d"%(i, len(subdirs)))
        for root,dirs,files in os.walk(subdir):
            for j, filename in enumerate(files):
                #print("%d file  out of %d"%(j, len(files)))
                with open(subdir+"/"+filename,"rb") as f:
                    completeQuote = pickle.load(f)
                quotes.update([completeQuote])
    corpus = Corpus(quotes)
    with open("/home/kuculo/quotekg/corpus/corpus.pkl","wb") as f:
        pickle.dump(corpus, f)

def change_to_umbrella_quotes(completeQuote):
    new_quotes = dict()
    for language in completeQuote.quotes:
        if language not in new_quotes:
            new_quotes[language] = []
        for quote in completeQuote.quotes[language]:
            umbrella_quote = umbrellaQuote(quote)
            new_quotes[language].append(umbrella_quote)
    completeQuote.quotes = new_quotes
    return completeQuote
            
def convert_to_umbrella_corpus():
    new_quotes = dict()
    corpus_file="/home/kuculo/quotekg/corpus/corpus.pkl"
    output = "/home/kuculo/quotekg/corpus/corpus_v2.pkl"
    with open(corpus_file,"rb") as f:
        corpus = pickle.load(f)
    for i, id in enumerate(corpus.completeQuotes):
        if i%1000==0:
            print("%d out %d converted"%(i, len(corpus.completeQuotes)))
        new_quotes.update({id:change_to_umbrella_quotes(corpus.completeQuotes[id])})
    corpus.completeQuotes = new_quotes
    """
    languages = []
    for id in corpus.completeQuotes:
        for language in corpus.completeQuotes[id].quotes:
             languages.append(language)
    for language in languages:
        if language in ["en","de","it"]:
            continue
        corpus.completeQuotes[id].quotes.pop(language, None)
    """
    with open(output, "wb") as f:
        pickle.dump(corpus, f)

def evaluate(corpus_path="/home/kuculo/quotekg/corpus/0.8/corpus_v2.pkl",input_id="Q7186", labels=None):
    with open(corpus_path,"rb") as f:
        corpus = pickle.load(f)
    quote_clusters = corpus.quotesById[input_id]
    return
from scipy.spatial import distance

#XLM-R
def evalClustering(entity, model, filter):
    entities = entity.entities
    X = []
    Y = []
    for language in entities:
        if entities[language][0].quotes:
            temp = [quote for quote in list(entities[language][0].quotes.values()) if quote.about==False]
            Y.append(temp)
    Y = [y for y in Y if y]
    for quotes in Y:
        temp = []
        for quote in quotes:
            try:
                temp.append(quote.embedding)#model.encode(quote.quote))#
            except TypeError:
                print(quote.id)
        X.append(temp)
    X = [x for x,_ in sorted(zip(X,Y), key=lambda pair: len(pair[1]), reverse=True)]
    Y.sort(key=len, reverse=True)
    f = open(entity.wikidata_id+"_dist.txt","w")
    for i, x in enumerate(X[:-1]):
        tree = BallTree(x, leaf_size=30, metric=my_distance)       
        for quotes, quote_embeddings in zip(Y[i+1:],X[i+1:]):
            for quote, quote_embedding in zip(quotes, quote_embeddings):
                if quote.language not in filter:
                    continue
                quote_embedding = quote_embedding.reshape(1,-1)
                #quote_embedding = model.encode(quote.quote).reshape(1,-1)
                dist, ind = tree.query(quote_embedding, k=1)
                dist = dist[0][0]
                ind = ind[0][0]
                sim = 1-dist
                if Y[i][ind].language not in filter:
                        continue
                f.write("\n")
                s = "\n1: "+quote.quote+"\n2: "+Y[i][ind].quote+"\ndist: "+str(dist)+"\nsim: "+str(sim)+"\n\n"
                f.write(s)

def cos_distance(a,b):
    return 1-distance.cosine(a,b)
     
def resolve_conflicts(connected_components):
    for cluster in connected_components:
        X = []
        for quote in cluster:
            if quote.page_language not in X:
                X.append(quote.page_language)
            else:
                return

     