import os
import re
import random

def find_java_files(folder_path):
    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    return java_files

def read_file_with_encoding(file_path):
    encodings = ['utf-8', 'cp949', 'euc-kr']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to read the file {file_path} with any of the attempted encodings")

def parse_java_file(file_path):
    content = read_file_with_encoding(file_path)
    # 간단한 메소드 파싱 (실제 구현에서는 더 복잡한 파싱이 필요할 수 있습니다)
    methods = re.findall(r'(\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\})', content)
    return methods

def obfuscate_method(method):
    # 메소드를 여러 블록으로 분할
    blocks = method.split(';')
    
    # 각 블록에 레이블 할당
    labeled_blocks = [f'case {i}: {block.strip()}; break;' for i, block in enumerate(blocks) if block.strip()]
    
    # 난독화된 메소드 구성
    obfuscated = f"""
    int state = 0;
    while(true) {{
        switch(state) {{
            {' '.join(labeled_blocks)}
            default: return;
        }}
    }}
    """
    return obfuscated

def obfuscate_java_file(file_path):
    content = read_file_with_encoding(file_path)
    
    methods = parse_java_file(file_path)
    for method in methods:
        obfuscated_method = obfuscate_method(method)
        content = content.replace(method, obfuscated_method)
    
    obfuscated_file_path = file_path.replace('.java', '_obfuscated.java')
    with open(obfuscated_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return obfuscated_file_path

def main():
    folder_path = 'C:/Users/sangbin/OneDrive/바탕 화면/vscode4/java-christmas-6-scienceNH/src/main/java/christmas'
    java_files = find_java_files(folder_path)
    
    for file in java_files:
        try:
            obfuscated_file = obfuscate_java_file(file)
            print(f"난독화된 파일 생성: {obfuscated_file}")
        except UnicodeDecodeError as e:
            print(f"파일 {file}을 처리하는 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()