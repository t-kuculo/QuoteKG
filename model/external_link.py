class ExternalLink:

    def __init__(self, uri):
        self.uri = uri
        self.text = None

    def print(self, level):
        print(" "*level + "External Link: " + self.uri)