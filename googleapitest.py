import requests
from bs4 import BeautifulSoup
import pickle

def get_relevance(query):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    URL     = "https://www.google.com/search?q="+query
    result = requests.get(URL, headers=headers)    

    soup = BeautifulSoup(result.content, 'html.parser')

    total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False) # this will give you the outer text which is like 'About 1,410,000,000 results'
    results_num = ''.join([num for num in total_results_text if num.isdigit()]) # now will clean it up and remove all the characters that are not a number .
    print(results_num)

with open("/home/kuculo/quotekg/corpus/corpus_v2.pkl","rb") as f:
    corpus = pickle.load(f)

for quote_id, completeQuote in corpus.completeQuotes.items():
        for language in completeQuote.quotes:
            for quote in completeQuote.quotes[language]:
                print(quote.quote)
                print(get_relevance(quote.quote))
                print("---")