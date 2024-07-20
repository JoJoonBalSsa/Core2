import javalang
import os
import base64
from aes import AES

class Encrypt_str:
    def __init__(self, encryption_key=None):
        self.encryption_key = encryption_key or os.urandom(16).hex()
    
    def parse_java_files(self, folder_path): # 소스코드 => AST tree
        java_files = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        source_code = file.read()
                    tree = javalang.parse.parse(source_code)
                    java_files.append((file_path, tree, source_code))
        return java_files

    def extract_string_literals(self, tree): # AST 에서 문자열 찾아내고 문자열 값과 위치 저장
        string_literals = []
        for path, node in tree:
            if isinstance(node, javalang.tree.Literal) and isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
                string_literals.append((node.value, node.position))
        return string_literals

    def encrypt_string_literals(self, string_literals): # 암호화 여기를 우리의 암호화 알고리즘으로 바꿔야함. 지금은 base64
        aes = AES()
        encrypted_literals = [aes.encrypt_string(literal.encode('utf-8'), self.encryption_key) for literal, _ in string_literals]
        return encrypted_literals

    def replace_string_literals(self, source_code, string_literals, class_name):
        lines = source_code.split('\n')
        string_literals_sorted = sorted(string_literals, key=lambda x: (x[1][0], -x[1][1]))  # 라인 오른쪽부터 문자열 변환
        for index, (literal, position) in enumerate(string_literals_sorted):
            line_index = position[0] - 1
            column_index = position[1] - 1
            line = lines[line_index]
            end_column_index = column_index + len(literal)
            new_line = line[:column_index] + f'STRING_LITERALS_{class_name.upper()}[{index}]' + line[end_column_index:]
            lines[line_index] = new_line
        return '\n'.join(lines)

    def insert_encrypted_string_array(self, source_code, encrypted_literals, class_name, class_position): # 문자열이 원래 있던 자리를 배열참조로 바꿈
        array_declaration = f'public static final String[] STRING_LITERALS_{class_name.upper()} = {{\n' + ',\n'.join(f'"{literal}"' for literal in encrypted_literals) + '\n};\n'
        lines = source_code.split('\n')
        lines.insert(class_position, array_declaration)
        return '\n'.join(lines)

    def process_java_files(self, java_files):
        for file_path, tree, source_code in java_files:
            class_declarations = []
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration): #클래스 별로 문자열을 추출할것이기 때문에 클래스 정의 위치 알아냄
                    class_declarations.append((node.name, node.position[0]))

            for class_name, class_position in class_declarations:
                string_literals = self.extract_string_literals(tree) # 클래스에 존재하는 문자열들 추출
                if not string_literals:
                    continue

                encrypted_literals = self.encrypt_string_literals(string_literals) #문자열들 암호화

                updated_source_code = self.replace_string_literals(source_code, string_literals, class_name) #문자열 -> 배열참조

                updated_source_code = self.insert_encrypted_string_array(updated_source_code, encrypted_literals, class_name, class_position) #소스코드에 배열 삽입
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_source_code)


def main():
    java_folder_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/test'  
    
    encryptor = Encrypt_str()
    java_files = encryptor.parse_java_files(java_folder_path) 
    
    encryptor.process_java_files(java_files) 

if __name__ == "__main__":
    main()
