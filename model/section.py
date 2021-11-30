class Section:

    def __init__(self):
        self.sub_sections = []
        self.lines = []
        self.templates = []
        self.title = None
        self.chronological = None


    def print(self, level=0):

        print(" " * level + "Section")

        if self.title:
            self.title.print(level, "Title")

        for line in self.lines:
            line.print(level + 1)

        for template in self.templates:
            template.print(level + 1)

        for section in self.sub_sections:
            section.print(level + 1)
