class Template:

    def __init__(self, type):
        self.type = type
        self.empty_values = []
        self.values = {}
        self.sub_templates = {}

    def print(self, level, prefix="Template"):
        print(" " * level + prefix + ": " + self.type)
        if self.empty_values:
            print(" " * (level + 1) + "Empty values: " + str(self.empty_values))
        for key, value in self.values.items():
            value.print(level + 1, "Sub line (" + key + ")")
        for key, sub_template in self.sub_templates.items():
            sub_template.print(level + 1, "Sub template (" + key + ")")
