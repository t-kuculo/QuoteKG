# [QuoteKG](http://quotekg.l3s.uni-hannover.de)

This is the code for creating QuoteKG, a multilingual knowledge graph of quotations. QuoteKG includes nearly one million quotes in 52 languages, said by more than 63,000 people of public interest across a wide range of topics.

### [WikiquoteDumper](https://github.com/sgottsch/WikiquoteDumper)
Use the WikiquoteDumper first to download Wikiquote dumps in any languages and convert them into JSON format.

#### Steps
* Run WikiquoteDumper to get language specific json files containing all the quotes
* Run main.py to create the quotation corpus pickle file
* Run xx to create the knowledge graph triples
* Run evaluation.py to get the F1 scores for the quote alignments 
