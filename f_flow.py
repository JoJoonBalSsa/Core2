#대상폴더경로불러오기
import os
import hashlib
import re
import sqlite3

# Java 파일들이 있는 폴더 경로
def get_java_files_path(project_root):
    java_path = os.path.join(project_root, 'java')
    if not os.path.exists(java_path):
        raise FileNotFoundError(f"Java 폴더가 존재하지 않습니다: {java_path}")
    return java_path

#대상파일읽기
def read_java_files(java_files_path):
    java_files = []
    for root, dirs, files in os.walk(java_files_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    java_files.append((file_path, f.read()))
    return java_files

#파일 내 함수 이름 및 기타 등등 읽기 및 db저장
def extract_function_names(file_content):
    # 간단한 함수 이름 추출 정규식 (단순화를 위해)
    function_pattern = re.compile(r'\bpublic\b|\bprivate\b|\bprotected\b.*?\b(\w+)\s*\(.*?\)\s*\{')
    return function_pattern.findall(file_content)

def save_to_db(java_files):
    conn = sqlite3.connect('function_meta.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS functions 
                 (file_path TEXT, function_name TEXT)''')
    
    for file_path, content in java_files:
        function_names = extract_function_names(content)
        for name in function_names:
            c.execute("INSERT INTO functions (file_path, function_name) VALUES (?, ?)", 
                      (file_path, name))
    
    conn.commit()
    conn.close()

#db읽기
def load_from_db():
    conn = sqlite3.connect('function_meta.db')
    c = conn.cursor()
    c.execute("SELECT * FROM functions")
    functions = c.fetchall()
    conn.close()
    return functions

#함수흐름난독화
#함수분할
def obfuscate_function_name(function_name):
    return hashlib.md5(function_name.encode()).hexdigest()[:8]

def obfuscate_java_file(content, function_map):
    for original_name, obfuscated_name in function_map.items():
        content = re.sub(r'\b' + original_name + r'\b', obfuscated_name, content)
    return content

#파일변경 및 저장
def apply_obfuscation(java_files, functions):
    function_map = {func[1]: obfuscate_function_name(func[1]) for func in functions}

    for file_path, content in java_files:
        obfuscated_content = obfuscate_java_file(content, function_map)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_content)

project_root = 'C:/Users/sangbin/OneDrive/바탕 화면/vscode4/java-christmas-6-scienceNH/src/test/java/christmas'

java_files_path = get_java_files_path(project_root)
java_files = read_java_files(java_files_path)
save_to_db(java_files)
functions = load_from_db()
apply_obfuscation(java_files, functions)