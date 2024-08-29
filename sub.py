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
1.메서드의 위치와 선언입니다. 이 메서드는 클래스에 속해 있지 않고, 독립적으로 선언 -> 변환된 메서드 아래에 삽입하도록 만듬
2.메서드의 반환 타입 return시 void로만 되어 문제가 됨 -> 메서드 인식시 자료형도 같이 가져오도록 만들고, 함수를 생성시 삽입
3.함수 삽입시 return이 삭제 되고 함수만 호출되어 문제가 됨 ->리턴 메서드일 시 메서드 본문 삭제 후 return과 함께 함수 호출
'''

#자바 파일들 불러오기
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

        method_body = java_content[start_index:end_index].strip()
        methods[method_name] = (method_body, start_index, end_index, return_type)

    return methods

#2번
def identify_java_structures(java_content):
    """
    자바 코드에서 for문, if문, 연산자를 식별합니다.

    :param java_content: 자바 파일의 전체 내용 (문자열)
    :return: 식별된 for문, if문, 연산자가 포함된 라인의 리스트
    """
    # 정규 표현식 패턴 정의
    for_pattern = re.compile(r'\bfor\s*\(.*\)')
    if_pattern = re.compile(r'\bif\s*\(.*\)')
    operators_pattern = re.compile(r'[+\-*/=><!]=?|&&|\|\|')

    # 결과를 저장할 리스트
    identified_lines = []

    # 각 라인별로 검사
    lines = java_content.splitlines()
    for idx, line in enumerate(lines):
        if for_pattern.search(line):
            identified_lines.append((idx + 1, "for", line.strip()))
        elif if_pattern.search(line):
            identified_lines.append((idx + 1, "if", line.strip()))
        elif operators_pattern.search(line):
            identified_lines.append((idx + 1, "operator", line.strip()))

    return identified_lines

#3번 랜덤이름
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


#5번
def replace_method_body_with_call(java_content, method_name, function_name, start_index, end_index, return_type):
    # 본문을 삭제하고 함수 호출로 대체
    if return_type == 'void':
        modified_content = (
            java_content[:start_index] +
            f"\n        {function_name}();" +
            java_content[end_index:]
        )
    else:
        modified_content = (
            java_content[:start_index] +
            f"\n        return {function_name}();" +
            java_content[end_index:]
        )
    return modified_content


#6번
def insert_func_below_method(java_content, new_func, end_index):
    # 메서드 끝난 지점 다음에 삽입
    lines = java_content.splitlines()
    insert_position = end_index

    # 삽입할 위치에 새로운 함수 코드 삽입
    lines.insert(insert_position, new_func)
    
    return "\n".join(lines)

# 파일 저장
def save_java_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
def main():
    folder_path = 'D:/vscode/vscode4/java-christmas-6-scienceNH/src/main/java/christmas'
    java_files = find_java_files(folder_path)
    
    for java_file in java_files:
        java_content = read_file_with_encoding(java_file)  # 파일 읽기

        methods = find_body(java_file)  # 1번
        for method_name, (method_body, start_index, end_index, return_type) in methods.items():
            new_func, new_func_name = generate_java_function(method_body, return_type)  # 3번, 4번

            # 5번: 기존 메서드에 있는 본문을 삭제하고 새 함수 호출 삽입
            modified_content = replace_method_body_with_call(java_content, method_name, new_func_name, start_index, end_index, return_type)

            # 6번: 새 함수를 기존 메서드 아래에 삽입
            final_content = insert_func_below_method(modified_content, new_func, end_index)

            # 수정된 파일 저장
            save_java_file(java_file, final_content)

if __name__ == "__main__":
    main()