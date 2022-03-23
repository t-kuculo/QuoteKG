
# https://databus.dbpedia.org/dbpedia/wikidata/sameas-all-wikis/
wget --no-check-certificate https://downloads.dbpedia.org/repo/dbpedia/wikidata/sameas-all-wikis/2021.09.01/sameas-all-wikis.ttl.bz2

bzip2 -d sameas-all-wikis.ttl.bz2


sed 's/<http:\/\/wikidata.dbpedia.org\/resource\///g;s/> <http:\/\/www.w3.org\/2002\/07\/owl#sameAs> </ /g;s/> .//g' sameas-all-wikis.ttl > sameas-all-wikis.csv


