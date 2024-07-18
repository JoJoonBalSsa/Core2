import javalang
import os
import base64

def parse_java_files(folder_path): # 소스코드 => AST tree
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

def extract_string_literals(tree): # AST 에서 문자열 찾아내고 문자열 값과 위치 저장
    string_literals = []
    for path, node in tree:
        if isinstance(node, javalang.tree.Literal) and isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
            string_literals.append((node.value, node.position))
    return string_literals

def encrypt_string_literals(string_literals): # 암호화 여기를 우리의 암호화 알고리즘으로 바꿔야함. 지금은 base64
    encrypted_literals = [base64.b64encode(literal.encode()).decode() for literal, _ in string_literals]
    return encrypted_literals

def replace_string_literals(source_code, string_literals, class_name):
    lines = source_code.split('\n')
    for index, (literal, position) in enumerate(string_literals):
        line_index = position[0] - 1
        column_index = position[1] - 1
        line = lines[line_index]
        # 만약 41 번째 라인의 내용 바꾼다면 아래 내용도 바꿔야함
        new_line = line[:column_index] + f'STRING_LITERALS_{class_name.upper()}[{index}]' + line[column_index + len(literal):]
        lines[line_index] = new_line
    return '\n'.join(lines)

def insert_encrypted_string_array(source_code, encrypted_literals, class_name, class_position): # 문자열이 원래 있던 자리를 배열참조로 바꿈
    # 지금은 STRING_LITERALS_{class 이름} 인데 바꿔도됨
    array_declaration = f'public static final String[] STRING_LITERALS_{class_name.upper()} = {{\n' + ',\n'.join(f'"{literal}"' for literal in encrypted_literals) + '\n};\n'
    lines = source_code.split('\n')
    lines.insert(class_position, array_declaration)
    return '\n'.join(lines)

def process_java_files(java_files):
    for file_path, tree, source_code in java_files:
        class_declarations = []
        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration): #클래스 별로 문자열을 추출할것이기 때문에 클래스 정의 위치 알아냄
                class_declarations.append((node.name, node.position[0]))

        for class_name, class_position in class_declarations:
            string_literals = extract_string_literals(tree) # 클래스에 존재하는 문자열들 추출
            if not string_literals:
                continue

            encrypted_literals = encrypt_string_literals(string_literals) #문자열들 암호화

            updated_source_code = replace_string_literals(source_code, string_literals, class_name) #문자열 -> 배열참조

            updated_source_code = insert_encrypted_string_array(updated_source_code, encrypted_literals, class_name, class_position) #소스코드에 배열 삽입
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_source_code)

def main():
    java_folder_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/test'  
    
    java_files = parse_java_files(java_folder_path) #자바 파일 파싱
    
    process_java_files(java_files) #문자열 추출 & 암호화 & 배열 삽입

if __name__ == "__main__":
    main()