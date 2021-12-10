import rdflib
from rdflib.namespace import OWL, RDF, RDFS, XSD
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

g.add((QKG.Mention, RDF.type, OWL.Class))
g.add((QKG.Mention, RDFS.label, Literal("quotation text", "en")))
g.add((QKG.Mention, RDFS.comment, Literal("An occurrence of a quotation", "en")))

g.add((QKG.Context, RDF.type, OWL.Class))
g.add((QKG.Context, RDFS.label, Literal("context", "en")))
g.add((QKG.Context, RDFS.comment, Literal("The context of a quotation occurrence", "en")))

g.add((QKG.hasMention, RDF.type, OWL.ObjectProperty))
g.add((QKG.hasMention, RDFS.domain, SO.Quotation))
g.add((QKG.hasMention, RDFS.range, QKG.Mention))

g.add((QKG.hasContext, RDF.type, OWL.ObjectProperty))
g.add((QKG.hasContext, RDFS.domain, QKG.Mention))
g.add((QKG.hasContext, RDFS.range, QKG.Context))

g.add((QKG.isMisattributed, RDF.type, OWL.DatatypeProperty))
g.add((QKG.isMisattributed, RDFS.domain, SO.Quotation))
g.add((QKG.isMisattributed, RDFS.range, XSD.boolean))

g.add((QKG.contextText, RDF.type, OWL.DatatypeProperty))
g.add((QKG.contextText, RDFS.domain, QKG.Context))
g.add((QKG.contextText, RDFS.range, RDF.langString ))

g.add((QKG.mentions, RDF.type, OWL.ObjectProperty))
g.add((QKG.mentions, RDFS.domain, QKG.Context))

print(g.serialize(format='ttl'))