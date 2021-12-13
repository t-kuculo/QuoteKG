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

def cluster(quotes, indices, completeEntity, path):
    if not os.path.isdir(path):
        os.mkdir(path)
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

def give_better_dates_to_completeQuotes(quote_dir, improved_clustered_quotes_path):
    if not os.path.isdir(improved_clustered_quotes_path):
        os.mkdir(improved_clustered_quotes_path)
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
                    #completeQuote.entity = None
                new_quote_dir = improved_clustered_quotes_path
                new_path = new_quote_dir+"/"+subdir.split("/")[-1]
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                with open(new_path+"/"+filename,"wb") as f:
                    pickle.dump(completeQuote, f)

def create_corpus(quote_dir, corpus_path):
    print("creating corpus")
    if not os.path.isdir(corpus_path):
        os.mkdir(corpus_path)
    corpus_path += "corpus.pkl"
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
    with open(corpus_path,"wb") as f:
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
            
def convert_to_umbrella_corpus(corpus_path):
    new_quotes = dict()
    corpus_file = corpus_path+ "/corpus.pkl"
    #output = "/corpus_v2.pkl"
    output = corpus_file
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

