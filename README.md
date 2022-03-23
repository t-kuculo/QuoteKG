# [QuoteKG](http://quotekg.l3s.uni-hannover.de)

This is the code for creating QuoteKG, a multilingual knowledge graph of quotations. QuoteKG includes nearly one million quotes in 52 languages, said by more than 63,000 people of public interest across a wide range of topics.

### [WikiquoteDumper](https://github.com/sgottsch/WikiquoteDumper)
Use the WikiquoteDumper first to download Wikiquote dumps in any languages and convert them into JSON format.

### Steps
Each step produces intermediate files that can be changed with alterations to the parameters.
<!-- #### Getting the initial data  --> 
<!-- #### Preprocessing  --> 
<!-- #### Evaluation  --> 
<!-- #### Alignment  --> 
<!-- #### Knowledge Graph creation  -->
* Run [WikiquoteDumper](https://github.com/sgottsch/WikiquoteDumper) to get language specific json files containing all the quotes
* Run the [WikiquoteToWikidataMapCreator ](https://github.com/sgottsch/WikiquoteDumper/blob/main/src/de/l3s/cleopatra/quotekg/data/WikiquoteToWikidataMapCreator.java) to get a mapping from Wikiquote to Wikidata IDs
* To separate the json files into files representing people and their quotes run ```python preprocessing.py``` 
* To create the quotation corpus pickle file run ```python main.py```
* To create a mapping between Wikidata IDs and DBpedia/Wikipedia IDs, run ```sh create_same_as_all_wikis.sh```
* To create the knowledge graph triples, update the parameters "current_date" and "file" in ```kg_creation.py``` and then run ```python kg_creation.py``` 
* To get the F1 scores for the quote alignment run ```python evaluation.py```
