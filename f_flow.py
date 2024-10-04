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
    pattern = r'\btry\s*\{'
    return bool(re.search(pattern, method_body))

#while검사
def has_while_in_body(method_body):
    # 정규표현식으로 while 구문 찾기
    pattern = r'\bwhile\s*\(.*?\)\s*\{'
    return bool(re.search(pattern, method_body))

def extract_variable_declarations(code):
    # 변수 선언 및 초기화 추출 (예: int x = 0;, String name = "test";)
    declaration_pattern = r'(\w+)\s+(\w+)\s*(=.*?);'
    declarations = re.findall(declaration_pattern, code)
    return declarations

def extract_statements_before_while(code):
    # while 블록 이전의 모든 구문 추출 (변수 선언이 아닌 일반 구문도 포함)
    statements_pattern = r'((?:.|\n)*?)\s*(while\s*\([^)]*\)\s*\{)'
    match = re.search(statements_pattern, code, re.DOTALL)
    if match:
        statements_before_while = match.group(1).strip()
        while_start = match.group(2).strip()
        return statements_before_while, while_start  # while 이전의 모든 구문과 while 시작 부분을 추출
    return code.strip(), ""  # while이 없는 경우 전체 코드 반환

def extract_while_block_content(java_code):
    # 메서드의 전체 구조를 캡처하는 정규식
    pattern = r'(public|private|protected)\s+(\w+)\s+(\w+)\s*\(.*?\)\s*\{(.*?)\s*while\s*\((.*?)\)\s*\{(.*?)\}(.*)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    
    if match:
        return_type = match.group(2)
        method_name = match.group(3)
        before_while_code = match.group(4).strip()
        while_condition = match.group(5).strip()
        while_content = match.group(6).strip()
        after_while_code = match.group(7).strip()

        # 변수 선언 추출
        declared_variables_before_while = extract_variable_declarations(before_while_code)
        
        # 모든 구문 추출
        statements_before_while, while_start = extract_statements_before_while(before_while_code)
        
        # `while` 구문을 완성해서 반환
        if not while_start:  # `while`이 추출되지 않았을 경우 수동으로 추가
            while_start = f"while ({while_condition}) {{"

        return while_content, return_type, method_name, declared_variables_before_while, while_condition, after_while_code, statements_before_while, while_start
    
    # None 값 8개 반환
    return None, None, None, None, None, None, None, None

#if검사
def has_if_in_body(method_body):
    return 'if' in method_body

def extract_for_block_content(java_code):
    pattern = r'for\s*\((.*?)\)\s*\{([\s\S]*?)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        condition = match.group(1).strip()
        content = match.group(2).strip()
        return condition, content
    return None, None

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

    if method_para:
        # Extract parameter names from method_para
        param_names = [param.split()[-1] for param in method_para.split(',')]
        params_string = ', '.join(param_names)
        
        if return_type == 'void':
            modified_body = f"\n        {function_name}({params_string});\n    "
        else:
            modified_body = f"\n        return {function_name}({params_string});\n    "
    else:
        if return_type == 'void':
            modified_body = f"\n        {function_name}();\n    "
        else:
            modified_body = f"\n        return {function_name}();\n    "
    modified_content = (
        java_content[:start_index] + modified_body + java_content[end_index-1:]
    )
    return modified_content

def if_try_catch(new_func):
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
    return new_method_content

def if_while_catch(new_func):
    # Extract content using the modified function
    while_content, return_type, method_name, declared_variables_before_while, while_condition, after_while_code, statements_before_while, while_start = extract_while_block_content(new_func)
    
    if while_content and return_type and method_name:
        # Extract each line in the while content
        lines = [line.strip() for line in while_content.splitlines() if line.strip()]
        
        method_calls = []
        new_methods = []
        method_count = 1

        # Extract method parameters
        parameters = new_func.split('(')[1].split(')')[0]
        param_list = [param.strip() for param in parameters.split(',') if param.strip()]
        parameter_names = ', '.join([param.split()[-1] for param in param_list])

        for line in lines:
            # Determine return type and parameters based on modified variables
            variable_to_modify = re.findall(r'(\w+)\s*(?:[+\-*/]?=)', line)
            if variable_to_modify:
                variable_to_modify = variable_to_modify[0]
                variable_type = None
                
                # Find type from declared variables
                for var_type, var_name, init_value in declared_variables_before_while:
                    if var_name == variable_to_modify:
                        variable_type = var_type
                        break
                
                # Find type from method parameters
                if not variable_type:
                    for param in param_list:
                        if variable_to_modify in param:
                            variable_type = param.split()[0]
                            break

                # Create a new function name
                new_func_name = generate_random_string()
                
                # Generate the new method with modified parameters and return type
                remaining_parameters = ', '.join([param for param in param_list if param.split()[-1] != variable_to_modify])
                if remaining_parameters:
                    new_method = f"""
    public {variable_type} {new_func_name}({variable_type} {variable_to_modify}, {remaining_parameters}) {{
        {line}
        return {variable_to_modify};
    }}
"""
                    method_calls.append(f"{variable_to_modify} = {new_func_name}({variable_to_modify}, {', '.join([param.split()[-1] for param in param_list if param.split()[-1] != variable_to_modify])});")
                else:
                    new_method = f"""
    public {variable_type} {new_func_name}({variable_type} {variable_to_modify}) {{
        {line}
        return {variable_to_modify};
    }}
"""
                    method_calls.append(f"{variable_to_modify} = {new_func_name}({variable_to_modify});")
            else:
                # Generate void method if no modified variable
                new_func_name = generate_random_string()
                new_method = f"""
    public void {new_func_name}({parameters}) {{
        {line}
    }}
"""
                method_calls.append(f"{new_func_name}({parameter_names});")
            
            new_methods.append(new_method)

        # Combine method calls into a single string
        method_calls_str = "\n            ".join(method_calls)

        # Extract and restore original variable declarations
        original_variable_declarations = extract_variable_declarations(new_func)

        # Only include variable declarations not already in statements_before_while
        variable_declarations = '; '.join([f'{var_type} {var_name} {init_value}' for var_type, var_name, init_value in original_variable_declarations if f'{var_name}' not in statements_before_while])
        variable_declarations = f"{variable_declarations};" if variable_declarations else ""

        # Restore the modified function
        modified_new_func = f"""
    public {new_func.split()[1]} {new_func.split()[2].split('(')[0]}({parameters}) {{
        {statements_before_while}
        {variable_declarations}
        {while_start}
            {method_calls_str}
        }}
        {after_while_code}
    }}
"""
        new_method_content = f"\n{modified_new_func}\n" + "\n".join(new_methods) + "\n"
    else:
        new_method_content = f"\n{new_func}\n"
    return new_method_content


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
    # print(new_func)
    if has_try_in_body(new_func):
        new_method_content = if_try_catch(new_func)
    elif has_while_in_body(new_func):
        new_method_content = if_while_catch(new_func)
    # elif has_for_in_body(new_func):
    #     pass
    # elif has_if_in_body(new_func):
    #     pass
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
        
        # save_file_with_encoding(java_file, java_content)
        # print(f"File saved: {java_file}")

if __name__ == "__main__":
    main()
