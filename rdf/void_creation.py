import rdflib
from rdflib.namespace import OWL, RDF, RDFS, XSD, VOID, FOAF, DCTERMS
from rdflib import Namespace
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from ns_QKG import QKG

import urllib

SO = Namespace("https://schema.org/")

g = Graph()
g.bind("qkg", QKG)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)
g.bind("void", VOID)
g.bind("foaf", FOAF)
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)

quotekg_uri = URIRef(QKG) + "QuoteKG"

g.add((quotekg_uri, RDF.type, VOID.Dataset))
g.add((quotekg_uri, FOAF.homepage, URIRef("https://quotekg.l3s.uni-hannover.de/")))
g.add((quotekg_uri, VOID.sparqlEndpoint, URIRef("https://quotekg.l3s.uni-hannover.de/sparql")))

g.add((quotekg_uri, DCTERMS.title, Literal("QuoteKG")))
g.add((quotekg_uri, DCTERMS.description, Literal("QuoteKG is a multilingual knowledge graph of quotations from famous "
                                                 "people.", "en")))

g.add((quotekg_uri, DCTERMS.publisher, URIRef("https://www.l3s.de/home")))
g.add((quotekg_uri, DCTERMS.creator, URIRef("https://www.l3s.de/~kuculo/")))
g.add((quotekg_uri, DCTERMS.creator, URIRef("https://www.l3s.de/~gottschalk/")))

g.add((quotekg_uri, DCTERMS.created, Literal("2020-04-20", datatype=XSD.date)))
g.add((quotekg_uri, DCTERMS.modified, Literal("2020-12-07", datatype=XSD.date)))

g.add((quotekg_uri, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by-sa/4.0/")))

languages = "it", "en", "pl", "ru", "cs", "fa", "de", "et", "pt", "fr", "uk", "es", "he", "sk", "tr", "bs", "ca", "eo", "fi", "az", "sl", "lt", "zh", "ar", "bg", "hy", "hr", "el", "su", "nn", "id", "sv", "li", "hu", "ko", "nl", "ja", "la", "ta", "sah", "sr", "gu", "gl", "ur", "te", "be", "cy", "no", "ml", "sq", "vi", "kn", "ro", "eu", "ku", "uz", "hi", "th", "ka", "da", "sa", "is"
for language in languages:
    g.add((quotekg_uri, DCTERMS.source, URIRef("https://" + language + ".wikiquote.org/")))

print(g.serialize(format='ttl'))
