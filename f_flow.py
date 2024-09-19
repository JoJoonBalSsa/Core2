import javalang
import os
import re
import random
import string
import secrets


'''
1. body부분 식별(메서드 이름과 body부분 코드 반환)
2. 조건문,반복문,연산,함수호출 식별
3. 새로운 함수만들기
4. 새로운 함수에 메서드의 body부분 복사
5. 복사한 메서드에 새로운 함수 호출
6. 만들어진 새로운 함수 java코드 상위에 붙여넣기

----고도화때 필요한 사항----
2번 함수 생성 및 관련사항
'''

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
#1번
def find_body(java_file_path):
    with open(java_file_path, 'r', encoding='utf-8') as file:
        java_content = file.read()

    method_pattern = re.compile(r'\b(public|protected|private)\s+(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{')
    methods = {}

    for match in method_pattern.finditer(java_content):
        access_modifier = match.group(1)
        return_type = match.group(2)
        method_name = match.group(3)
        parameters = match.group(4)
        start_index = match.end()

        open_braces = 1
        end_index = start_index
        while open_braces > 0 and end_index < len(java_content):
            if java_content[end_index] == '{':
                open_braces += 1
            elif java_content[end_index] == '}':
                open_braces -= 1
            end_index += 1

        method_body = java_content[start_index:end_index-1].strip()
        methods[method_name] = (return_type, parameters, method_body)

    return methods
#2번
#try-catch
def extract_try_block_content(java_code):
    pattern = r'(public|private)\s+(\w+)\s+\w+\s*\([^)]*\)\s*\{.*?try\s*\{([\s\S]*?)\s*return\s+(.*?);'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        return_type = match.group(2)
        content = match.group(3).strip()
        return_value = match.group(4).strip()
        return content, return_value, return_type
    return None, None, None
#try검사
def has_try_in_body(method_body):
    return 'try' in method_body

def extract_while_block_content(java_code):
    pattern = r'(public|private)'
    match = re.search(pattern, java_code, re.DOTALL)

#while검사
def has_while_in_body(method_body):
    return 'while' in method_body

def extract_if_block_content(java_code):
    pattern = r'(public|private)'
    match = re.search(pattern, java_code, re.DOTALL)

#if검사
def has_if_in_body(method_body):
    return 'if' in method_body

def extract_for_block_content(java_code):
    pattern = r'(public|private)'
    match = re.search(pattern, java_code, re.DOTALL)

#for검사
def has_for_in_body(method_body):
    return 'for' in method_body

def generate_random_string(length=8):
    if length < 1:
        raise ValueError("Length must be at least 1")
    letters = string.ascii_lowercase
    letters_and_digits = string.ascii_lowercase + string.digits
    first_char = secrets.choice(letters)
    rest_chars = ''.join(secrets.choice(letters_and_digits) for _ in range(length - 1))
    
    return first_char + rest_chars

#3번, 4번
def generate_java_function(method_body, return_type, method_para):
    function_name = generate_random_string()
    java_function_code = f"""
    public {return_type} {function_name}({method_para}) {{
    {method_body}
}}
"""
    return java_function_code, function_name

#5번
def replace_method_body(java_content, method_name, function_name, return_type, method_para):
    method_pattern = re.compile(rf"(\b{return_type}\s+{method_name}\s*\([^)]*\)\s*{{)")
    
    match = method_pattern.search(java_content)
    if not match:
        print(f"Method {method_name} not found in the Java content.")
        return None
    
    start_index = match.end()
    
    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1

    if method_para != '':
        para = method_para.split()[1]
        if return_type == 'void':
            modified_body = f"\n        {function_name}({para});\n"
        else:
            modified_body = f"\n        return {function_name}({para});\n"
    else:
        if return_type == 'void':
            modified_body = f"\n        {function_name}();\n"
        else:
            modified_body = f"\n        return {function_name}();\n"
    
    modified_content = (
        java_content[:start_index] + modified_body + java_content[end_index-1:]
    )
    
    return modified_content
#6번
def add_new_method(java_content, method_name, new_func):
    method_pattern = re.compile(rf"\b\S+\s+{method_name}\s*\([^)]*\)\s*{{")
    
    match = method_pattern.search(java_content)
    if not match:
        print(f"Method {method_name} not found in the Java content.")
        return None
    
    start_index = match.end()
    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1

    if has_try_in_body(new_func):
        try_content, return_value, return_type = extract_try_block_content(new_func)
        if try_content and return_value and return_type:
            new_func_name = generate_random_string()
            
            new_try_func = f"""
    public {return_type} {new_func_name}({new_func.split('(')[1].split(')')[0]}) {{
        {try_content}
        return {return_value};
    }}
"""
            modified_new_func = f"""
    public {new_func.split()[1]} {new_func.split()[2].split('(')[0]}({new_func.split('(')[1].split(')')[0]}) {{
        try {{
            return {new_func_name}({new_func.split('(')[1].split(')')[0].split()[-1]});
        }} catch (IllegalArgumentException e) {{
            return {return_value};
        }}
    }}
"""
            new_method_content = f"\n{modified_new_func}\n{new_try_func}\n"
        else:
            new_method_content = f"\n{new_func}\n"
    elif has_while_in_body(new_func):
        pass
    elif has_for_in_body(new_func):
        pass
    elif has_if_in_body(new_func):
        pass
    else:
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
        java_content = read_file_with_encoding(java_file)

        methods = find_body(java_file)
        for method_name, (return_type, method_para, method_body) in methods.items():
            print(f"Processing file: {java_file}")
            
            new_func, new_func_name = generate_java_function(method_body, return_type, method_para)
            
            java_content = replace_method_body(java_content, method_name, new_func_name, return_type, method_para)
            
            java_content = add_new_method(java_content, method_name, new_func)
        
        save_file_with_encoding(java_file, java_content)
        print(f"File saved: {java_file}")

if __name__ == "__main__":
    main()