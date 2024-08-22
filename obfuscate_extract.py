import re

class JavaControlFlowExtractor:
    def __init__(self, java_code):
        self.java_code = java_code

    def find_if_conditions(self):
        if_pattern = re.compile(r'\bif\s*\((.*?)\)\s*\{', re.DOTALL)
        return if_pattern.findall(self.java_code)

    def find_for_conditions(self):
        for_pattern = re.compile(r'\bfor\s*\((.*?)\)\s*\{', re.DOTALL)
        return for_pattern.findall(self.java_code)

    def find_while_conditions(self):
        while_pattern = re.compile(r'\bwhile\s*\((.*?)\)\s*\{', re.DOTALL)
        return while_pattern.findall(self.java_code)

    def find_do_while_conditions(self):
        do_while_pattern = re.compile(r'\bdo\s*\{.*?\}\s*while\s*\((.*?)\);', re.DOTALL)
        return do_while_pattern.findall(self.java_code)

    def extract_all_conditions(self):
        expressions = []
        expressions.append(self.find_if_conditions())
        expressions.append(self.find_for_conditions())
        expressions.append(self.find_while_conditions())
        expressions.append(self.find_do_while_conditions())

        return expressions