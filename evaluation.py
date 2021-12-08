import pickle

from networkx.algorithms.centrality.current_flow_betweenness import edge_current_flow_betweenness_centrality
from model.entity_quotes import *
from model.complete_quote import *
from model.utils import *
from itertools import *

our_languages = ["en", "it", "de"]
our_languages.reverse()

folder = "data/ground_truth"
corpus_filename = "corpus/corpus_v2.pkl"

ground_truth = dict()
clusters = dict()

ground_truth_entities = {"Q105167": "Tom Clancy", "Q57661": "Jean-Claude Juncker", "Q13424289": "Edward Snowden",
                         "Q7251": "Alan Turing", "Q47365": "Marie Antoinette", "Q7304": "Gustav Mahler",
                         "Q8409": "Alexander the Great", "Q7186": "Marie Curie"}

# collect pairs of aligned and pairs of unaligned quotations from ground truth
for filename in os.listdir(folder):
    if filename.endswith(".tsv"):
        wikidata_id = filename.replace(".tsv", "")
        print("Wikidata ID", wikidata_id)

        ground_truth[wikidata_id] = dict()
        clusters[wikidata_id] = dict()

        file = open(folder + "/" + filename)
        all_texts = set()
        ground_truth_tps = set()
        ground_truth_tns = set()

        ground_truth[wikidata_id]["tps"] = ground_truth_tps
        ground_truth[wikidata_id]["tns"] = ground_truth_tns
        ground_truth[wikidata_id]["all"] = all_texts

        clusters[wikidata_id]["unclustered"] = set()
        clusters[wikidata_id]["clustered"] = set()
        clusters[wikidata_id]["all"] = set()

        for line in file:
            parts = line.split("\t")
            parts = list(map(lambda s: s.strip(), parts))

            for part in parts:
                part = part.strip()
                if part:
                    all_texts.add(part)

            for text1 in parts:
                text1 = text1.strip()
                if not text1:
                    continue
                for text2 in parts:
                    text2 = text2.strip()
                    if not text2:
                        continue
                    if text1 != text2:
                        # collect all pairs of quotations that are aligned
                        pair = frozenset((text1, text2))
                        ground_truth_tps.add(pair)

        # collect all pairs of quotations that are not aligned
        for text1 in all_texts:
            for text2 in all_texts:
                if text1 != text2:
                    pair = frozenset((text1, text2))
                    if pair not in ground_truth_tps:
                        ground_truth_tns.add(pair)

print("Load corpus", flush=True)
with open(corpus_filename, "rb") as f:
    corpus = pickle.load(f)

# load quotation clusters from our data
for completeQuote in corpus.completeQuotes.values():

    #completeEntity = completeQuote.entity

    #wikidata_id = completeEntity.wikidata_id
    wikidata_id = completeQuote.id.split("_")[0]
    if wikidata_id not in ground_truth.keys():
        continue

    quote_texts = set()
    if "en" in completeQuote.quotes.keys() or "de" in completeQuote.quotes.keys() or "it" in completeQuote.quotes.keys():
        print("###")
        if len(completeQuote.quotes.keys()) > 1:
            for lang, quotes in completeQuote.quotes.items():
                for quote in quotes:
                    print(lang,quote)
            print("###")
    for lang, quotes in completeQuote.quotes.items():
        
        for quote in quotes:

            if lang not in our_languages:
                continue

            quote_text = lang + ": " + quote.quote
            quote_text = quote_text.replace("\n", "")

            if quote_text in ground_truth[wikidata_id]["all"]:
                if quote_text not in clusters[wikidata_id]["all"]:
                    clusters[wikidata_id]["all"].add(quote_text)

                quote_texts.add(quote_text)
            #else:
                #print("$$$")
                #print(quote_text)

    for text1 in quote_texts:
        for text2 in quote_texts:
            if text1 == text2:
                continue
            pair = frozenset((text1, text2))
            clusters[wikidata_id]["clustered"].add(pair)

# collect pairs of quotations that are not within the same cluster
for wikidata_id in clusters.keys():
    for text1 in clusters[wikidata_id]["all"]:
        for text2 in clusters[wikidata_id]["all"]:
            if text1 != text2:
                pair = frozenset((text1, text2))
                if pair not in clusters[wikidata_id]["clustered"]:
                    clusters[wikidata_id]["unclustered"].add(pair)

# remove non-existing texts from ground truth (because we evaluate the clustering here, not the selection of quotations)
for wikidata_id in ground_truth.keys():
    for text in ground_truth[wikidata_id]["all"]:
        if text not in clusters[wikidata_id]["all"]:
            pairs_to_remove = set()
            for pair in ground_truth[wikidata_id]["tps"]:
                if text in pair:
                    pairs_to_remove.add(pair)
            ground_truth[wikidata_id]["tps"].difference_update(pairs_to_remove)
            pairs_to_remove = set()
            for pair in ground_truth[wikidata_id]["tns"]:
                if text in pair:
                    pairs_to_remove.add(pair)
            ground_truth[wikidata_id]["tns"].difference_update(pairs_to_remove)

# evaluation
average_f_score = 0
average_p = 0
average_r = 0
tp_total = 0
tn_total = 0
fp_total = 0
fn_total = 0

for wikidata_id in ground_truth.keys():

    print("wikidata_id:", wikidata_id)

    tps = ground_truth[wikidata_id]["tps"]
    tns = ground_truth[wikidata_id]["tns"]
    clustered = clusters[wikidata_id]["clustered"]
    unclustered = clusters[wikidata_id]["unclustered"]

    print("Ground truth, tps:", len(tps))
    print("Ground truth, tns:", len(tns))

    print("Clustered:", len(clustered))
    print("Unclustered:", len(unclustered))

    print("tps+tns:", len(tps) + len(tns))
    print("clustered+unclustered:", len(unclustered) + len(clustered))

    # TP: How many pairs that are in tps are also in clustered?
    tp = len(tps.intersection(clustered))
    print("TP:", tp)
    tp_total += tp

    tn = len(tns.intersection(unclustered))
    print("TN:", tn)
    tn_total += tn

    fp = len(clustered.difference(tps))
    print("FP:", fp)
    fp_total += fp

    fn = len(unclustered.difference(tns))
    print("FN:", fn)
    fn_total += fn

    print("Sum", tp + fp + tn + fn)

    if fp == 0:
        p = 1
    else:
        p = tp / (tp + fp)
    print("P", p)
    average_p += p

    r = tp / (tp + fn)
    print("R", r)
    average_r += r

    if tp == 0 and (fn > 0 or fp > 0):
        f = 0
    else:
        beta = 1
        f = ((beta ** 2 + 1) * p * r) / (beta ** 2 * p + r)
    average_f_score += f

    # LaTeX output
    print(ground_truth_entities[wikidata_id], "&", tp, "&", tn, "&", fp, "&", fn, "&", p, "&", r, "&", f)

    print("")

average_p = average_p / len(ground_truth.keys())
average_r = average_r / len(ground_truth.keys())
average_f_score = average_f_score / len(ground_truth.keys())
print("Average F score: ", average_f_score)
print("Average precision: ", average_p)
print("Average recall: ", average_r)
print("TP, total: ", tp_total)
print("TN, total: ", tn_total)
print("FP, total: ", fp_total)
print("FN, total: ", fn_total)

# LaTeX output
print(tp_total, "&", tn_total, "&", fp_total, "&", fn_total, "&", average_p, "&", average_r, "&", average_f_score)
