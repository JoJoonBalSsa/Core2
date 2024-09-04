import javalang
import random
import os
import glob
import re

class ob_identifier:
    def __init__(self,folder_path, output_directory):
        self.folder_path = folder_path
        self.output_directory = output_directory
        self.__process_java_files_in_folder__()

    def __generate_obfuscated_name__(self,length=8):
        ran = random.choice([1,2,3])
        if ran == 1:
            return ''.join(random.choices(["l","I"], k=1))+''.join(random.choices(['l', '1', 'I'], k=length))
        elif ran == 2:
            return ''.join(random.choices(['l', 'I', 'α', 'β', 'γ', 'δ', 'π'],k=1))+''.join(random.choices(['l', '1', 'I', 'α', 'β', 'γ', 'δ', 'π'],k=length))
        elif ran == 3:
            return ''.join(random.choices(['O','o'],k=1))+''.join(random.choices( ['0', 'O', 'o', 'Ο', 'о'],k=length))


    def __extract_user_defined_identifiers__(self,java_code):
        user_defined_classes = set()
        user_defined_methods = set()
        user_defined_variables = set()
        user_defined_imports = set()

        tokens = list(javalang.tokenizer.tokenize(java_code))
        parser = javalang.parser.Parser(tokens)
        tree = parser.parse()

        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                user_defined_classes.add(node.name)
                for body_item in node.body:
                    if isinstance(body_item, javalang.tree.MethodDeclaration):
                        user_defined_methods.add(body_item.name)
                        for param in body_item.parameters:
                            user_defined_variables.add(param.name)
                        if body_item.body is not None:
                            for statement in body_item.body:
                                if isinstance(statement, javalang.tree.VariableDeclarator):
                                    user_defined_variables.add(statement.name)
            elif isinstance(node, javalang.tree.MethodDeclaration):
                user_defined_methods.add(node.name)
                for param in node.parameters:
                    user_defined_variables.add(param.name)
                if node.body is not None:
                    for statement in node.body:
                        if isinstance(statement, javalang.tree.VariableDeclarator):
                            user_defined_variables.add(statement.name)
            elif isinstance(node, javalang.tree.VariableDeclarator):
                user_defined_variables.add(node.name)
            elif isinstance(node, javalang.tree.Import):
                if not node.path.startswith("java.") and not node.path.startswith("javax."):
                    user_defined_imports.add(node.path)

        return user_defined_classes, user_defined_methods, user_defined_variables, user_defined_imports

    def __create_identifier_mapping__(self,user_defined_classes, user_defined_methods, user_defined_variables):
        identifier_mapping = {}
        used_obfuscated_names = set()

        for identifier in user_defined_classes.union(user_defined_methods).union(user_defined_variables):
            obfuscated_name = self.__generate_obfuscated_name__()
            while obfuscated_name in used_obfuscated_names:
                obfuscated_name = self.__generate_obfuscated_name__()
            identifier_mapping[identifier] = obfuscated_name
            used_obfuscated_names.add(obfuscated_name)

        return identifier_mapping

    def __obfuscate_code_with_mapping__(self,java_code, identifier_mapping):
        obfuscated_code = java_code

        for identifier, obfuscated_name in identifier_mapping.items():
            if identifier != 'main': 
                obfuscated_code = re.sub(r'\b' + re.escape(identifier) + r'\b', obfuscated_name, obfuscated_code)

        return obfuscated_code

    def __process_java_files_in_folder__(self):
        all_user_defined_classes = set()
        all_user_defined_methods = set()
        all_user_defined_variables = set()

        java_files = glob.glob(os.path.join(self.folder_path, '**', '*.java'), recursive=True)

        for file_path in java_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                java_code = file.read()
                user_defined_classes, user_defined_methods, user_defined_variables, user_defined_imports = self.__extract_user_defined_identifiers__(java_code)
                all_user_defined_classes.update(user_defined_classes)
                all_user_defined_methods.update(user_defined_methods)
                all_user_defined_variables.update(user_defined_variables)

        identifier_mapping = self.__create_identifier_mapping__(all_user_defined_classes, all_user_defined_methods, all_user_defined_variables)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        for file_path in java_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                java_code = file.read()

            obfuscated_code = self.__obfuscate_code_with_mapping__(java_code, identifier_mapping)

            relative_path = os.path.relpath(file_path, self.folder_path)
            base_dir, original_filename = os.path.split(relative_path)
            original_class_name = original_filename.split('.')[0]

            new_class_name = identifier_mapping.get(original_class_name, original_class_name)

            new_filename = new_class_name + '.java'
            output_path = os.path.join(self.output_directory, base_dir, new_filename)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(obfuscated_code)

        print(identifier_mapping)
        return identifier_mapping