from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

class QKG(DefinedNamespace):
    _fail = True

    Mention: URIRef  # An occurrence of a quotation
    Context: URIRef  # The context of a quotation occurrence

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    hasMention: URIRef
    hasContext: URIRef
    isMisattributed: URIRef
    contextText: URIRef
    mentions: URIRef

    _NS = Namespace("https://quotekg.l3s.uni-hannover.de/resource/")
