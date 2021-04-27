# [QuoteKG](http://quotekg.l3s.uni-hannover.de)

This is the code for creating QuoteKG, a multilingual knowledge graph of quotations. QuoteKG includes nearly one million quotes in 52 languages, said by more than 63,000 people of public interest across a wide range of topics.

### [WikiquoteDumper](https://github.com/sgottsch/WikiquoteDumper)
Use the WikiquoteDumper first to download Wikiquote dumps in any languages and convert them into JSON format.

### Steps
#### Getting the initial data
* Run [WikiquoteDumper](https://github.com/sgottsch/WikiquoteDumper) to get language specific json files containing all the quotes
#### Preprocessing 
* To separate the json files into files representing people and their quotes run preprocessing.py 
#### Alignment
* To create the quotation corpus pickle file run main.py
#### Knowledge Graph creation
* To create the knowledge graph triples run kg_creation 
#### Evaluation
* To get the F1 scores for the quote alignment run evaluation.py 
