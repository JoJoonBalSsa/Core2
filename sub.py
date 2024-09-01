import javalang
import os
import re
import random
import string
'''
1. body부분 식별(메서드 이름과 body부분 코드 반환)
2. 조건문,반복문,연산,함수호출 식별
3. 새로운 함수만들기
4. 새로운 함수에 메서드의 body부분 복사
5. 복사한 메서드에 새로운 함수 호출
6. 만들어진 새로운 함수 java코드 상위에 붙여넣기

----수정이 필요한 사항----
2번 함수 생성 및 관련사항
'''

def find_java_files(folder_path):
    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
    return java_files

#파일 읽기
def read_file_with_encoding(file_path):
    encodings = ['utf-8', 'cp949', 'euc-kr']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to read the file {file_path} with any of the attempted encodings")

#1번
def find_body(java_file_path):
    with open(java_file_path, 'r', encoding='utf-8') as file:
        java_content = file.read()

    # 메서드 정의를 찾는 정규 표현식
    method_pattern = re.compile(r'\b(public|protected|private)\s+(\w+)\s+(\w+)\s*\([^)]*\)\s*\{')
    methods = {}

    for match in method_pattern.finditer(java_content):
        access_modifier = match.group(1)  # public, protected, private
        return_type = match.group(2)      # 반환 타입 (예: void, int 등)
        method_name = match.group(3)      # 메서드 이름
        start_index = match.end()

        open_braces = 1
        end_index = start_index
        while open_braces > 0 and end_index < len(java_content):
            if java_content[end_index] == '{':
                open_braces += 1
            elif java_content[end_index] == '}':
                open_braces -= 1
            end_index += 1

        # 메서드 본문에서 마지막 닫는 중괄호를 제외하고 추출
        method_body = java_content[start_index:end_index-1].strip()
        methods[method_name] = (method_body, return_type)

    return methods

#2번
def identify_java_structures(java_content):
    """
    자바 코드에서 for문, if문, 연산자를 식별합니다.

    :param java_content: 자바 파일의 전체 내용 (문자열)
    :return: 식별된 for문, if문, 연산자가 포함된 라인의 리스트
    """
    
    loop_pattern = re.compile(r'\b(for|while|foreach)\s*\(.*\)')

    if_pattern = re.compile(r'\b(if|else\s+if)\s*\(.*\)')
    operators_pattern = re.compile(r'[+\-*/=><!]=?|&&|\|\|')
    switch_case_pattern = re.compile(r'\b(switch|case)\b')
    do_while_pattern = re.compile(r'\bdo\s*{[^}]*}\s*while\s*\(.*\);')


    # 결과를 저장할 리스트
    identified_lines = []

    # 각 라인별로 검사
    lines = java_content.splitlines()
    for idx, line in enumerate(lines):
        if loop_pattern.search(line):
            identified_lines.append((idx + 1, "for", line.strip()))
        elif if_pattern.search(line):
            identified_lines.append((idx + 1, "if", line.strip()))
        elif operators_pattern.search(line):
            identified_lines.append((idx + 1, "operator", line.strip()))
        elif switch_case_pattern.search(line):
            identified_lines.append((idx + 1, "switch", line.strip()))
        elif do_while_pattern.search(line):
            identified_lines.append((idx + 1, "do_while", line.strip()))


    return identified_lines

def generate_random_string(length=8):
    """특정 길이의 랜덤 문자열을 생성합니다."""
    letters = string.ascii_lowercase + string.digits  # 소문자와 숫자로 구성
    first_char = random.choice(string.ascii_lowercase)  # 첫 문자는 소문자
    remaining_chars = ''.join(random.choice(letters) for _ in range(length - 1))
    return first_char + remaining_chars

#3번, 4번
def generate_java_function(method_body, return_type):
    function_name = generate_random_string()
    java_function_code = f"""
    public {return_type} {function_name}() {{
    {method_body}
}}
"""
    return java_function_code, function_name
import re

#5번
def replace_method_body(java_content, method_name, function_name, return_type):
    # 메서드 시그니처를 찾는 정규 표현식 (메서드 이름과 괄호, 매개변수 포함)
    method_pattern = re.compile(rf"(\b{return_type}\s+{method_name}\s*\([^)]*\)\s*{{)")
    
    # 메서드 시그니처의 위치를 찾습니다.
    match = method_pattern.search(java_content)
    if not match:
        raise ValueError(f"Method {method_name} not found in the Java content.")
    
    # 메서드 body의 시작 위치를 구합니다.
    start_index = match.end()
    
    # 메서드 body의 끝 위치를 찾기 위해 중괄호의 짝을 맞춥니다.
    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1
    
    # 새로운 메서드 body를 작성합니다.
    if return_type == 'void':
        modified_body = (
            f"\n        {function_name}();\n"
        )
    else:
        modified_body = (
            f"\n        return {function_name}();\n"
        )
    
    # 기존 메서드 body를 대체합니다.
    modified_content = (
        java_content[:start_index] + modified_body + java_content[end_index-1:]
    )
    
    return modified_content
#6번
def add_new_method(java_content, method_name, new_func):
    # 메서드 시그니처를 찾는 정규 표현식
    method_pattern = re.compile(rf"\b\S+\s+{method_name}\s*\([^)]*\)\s*{{")
    
    # 메서드 시그니처의 위치를 찾습니다.
    match = method_pattern.search(java_content)
    if not match:
        raise ValueError(f"Method {method_name} not found in the Java content.")
    
    # 메서드 끝 위치를 찾기 위해 중괄호의 짝을 맞춥니다.
    start_index = match.end()
    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1
    
    # 새로운 메서드를 추가합니다.
    new_method_content = f"\n{new_func}\n"
    modified_content = (
        java_content[:end_index] + new_method_content + java_content[end_index:]
    )
    
    return modified_content

def save_file_with_encoding(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
        
def main():
    folder_path = 'E:/f_flow/java-christmas-6-scienceNH/src/main/java/christmas'
    java_files = find_java_files(folder_path)
    
    for java_file in java_files:
        java_content = read_file_with_encoding(java_file)  # 파일 읽기

        methods = find_body(java_file)  # 1번
        for method_name, (method_body, return_type) in methods.items():
            print(f"Processing file: {java_file}")
            print(f"Modifying method: {method_name}")
            
            # 3번, 4번: 새 메서드 생성
            new_func, new_func_name = generate_java_function(method_body, return_type)
            
            # 5번: 기존 메서드 본문을 대체
            java_content = replace_method_body(java_content, method_name, new_func_name, return_type)
            
            # 6번: 새 메서드를 추가
            java_content = add_new_method(java_content, method_name, new_func)
        
        # 파일에 변경 내용 저장
        save_file_with_encoding(java_file, java_content)
        print(f"File saved: {java_file}")
            

if __name__ == "__main__":
    main()