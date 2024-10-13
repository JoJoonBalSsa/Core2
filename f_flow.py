import javalang
import os
import re
import random
import string
import secrets
import regex as re

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
def check_for_conditionals_loops(if_content):
    print(if_content)
    # 조건문과 반복문이 있는지 확인
    conditional_pattern = re.compile(r'if\s*\(.*?\)|while\s*\(.*?\)|for\s*\(.*?\)')
    return bool(conditional_pattern.search(if_content))
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
    pattern = r'\bif\s*\(.*?\)\s*\{'
    return bool(re.search(pattern, method_body))

def extract_method_components(java_code):
    method_pattern = re.compile(r'(public|private|protected)\s+(\w+)\s+(\w+)\((.*?)\)\s*\{', re.DOTALL)
    methods = method_pattern.finditer(java_code)
    
    method_data = []

    for method in methods:
        # 메서드 시그니처 및 본문 추출
        method_signature = method.group(0)
        method_body_start = method.end()  # 본문 시작 위치

        # 메서드 전체 본문 추출 (중괄호 짝 맞추기 방식)
        method_body = extract_full_body(java_code, method_body_start)
        
        # if문 추출 (중첩된 if문까지 처리)
        if_statement = extract_if_statement_with_brackets(method_body)
        
        method_data.append({
            'access_modifier': method.group(1),
            'return_type': method.group(2),
            'method_name': method.group(3),
            'parameters': method.group(4),
            'body': method_body,
            'if_content': if_statement
        })

    return method_data

def extract_if_statement_with_brackets(code):
    if_start = code.find('if')
    if if_start == -1:
        return None
    
    # 중괄호 짝 맞추기 시작
    stack = []
    body_start = code.find('{', if_start)
    if body_start == -1:
        return None
    
    stack.append('{')
    body_end = body_start + 1

    while stack and body_end < len(code):
        if code[body_end] == '{':
            stack.append('{')
        elif code[body_end] == '}':
            stack.pop()
        body_end += 1
    
    # if문 전체 반환
    return code[if_start:body_end].strip()

def extract_full_body(code, start):
    stack = []
    body_start = code.find('{', start)
    
    if body_start == -1:
        return None
    
    stack.append('{')
    body_end = body_start + 1
    
    while stack and body_end < len(code):
        if code[body_end] == '{':
            stack.append('{')
        elif code[body_end] == '}':
            stack.pop()
        body_end += 1
    
    return code[start:body_end]

def extract_conditionals_loops(if_content):
    # 첫 번째 if문 전체를 추출하고 그 내부에서 중첩된 if문을 다시 추출
    outer_if_pattern = re.search(r'(if|else\s*if|else|for|while|do)\s*\(.*?\)\s*\{(.*)', if_content, re.DOTALL)
    if outer_if_pattern:
        outer_if_content = outer_if_pattern.group(1)  # 첫 번째 if문의 내부 내용
        
        # 중괄호 짝 맞추기 방식으로 중첩된 if문 추출
        stack = []
        if_start = outer_if_content.find('if')
        
        if if_start != -1:
            # 중괄호 짝 맞추기 시작
            body_start = outer_if_content.find('{', if_start)
            if body_start == -1:
                return None
            
            stack.append('{')
            body_end = body_start + 1

            while stack and body_end < len(outer_if_content):
                if outer_if_content[body_end] == '{':
                    stack.append('{')
                elif outer_if_content[body_end] == '}':
                    stack.pop()
                body_end += 1
            
            # 중첩된 if문 전체를 반환
            return outer_if_content[if_start:body_end].strip()
    
    return None

def extract_if_statement(java_code):
    # `if` 문과 그 내부 내용을 추출하는 정규식
    pattern = r'if\s*\((.*?)\)\s*\{(.*?)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        condition = match.group(1).strip()
        content = match.group(2).strip()
        return condition, content
    return None, None

def extract_variables_before_if(java_code):
    # `if` 문이 나오기 전에 선언된 변수들을 추출
    lines = java_code.splitlines()
    variables = {}
    pattern = r'(int|String|double|float|char|boolean)\s+(\w+)\s*=\s*(.*);'

    for line in lines:
        line = line.strip()
        if re.match(r'if\s*\(', line):
            # `if` 문이 시작되면 그 전까지의 변수를 모두 처리
            break
        
        match = re.match(pattern, line)
        if match:
            var_type, var_name, expression = match.groups()
            variables[var_name] = var_type

    return variables

def extract_method_parameters(java_code):
    # 메서드 시그니처에서 파라미터와 타입을 추출
    parameters_match = re.search(r'\((.*?)\)', java_code)
    parameters = []
    parameter_types = {}
    if parameters_match:
        param_list = [param.strip() for param in parameters_match.group(1).split(',')]
        for param in param_list:
            if param:  # 파라미터가 존재할 때만 추가
                param_parts = param.rsplit(' ', 1)
                if len(param_parts) == 2:
                    param_type, param_name = param_parts
                    parameters.append(param_name)
                    parameter_types[param_name] = param_type
    return parameters, parameter_types

def extract_variables_in_if_statement(content, parameters):
    # `if` 문 내부에서 사용되는 변수 추출
    variable_pattern = r'\b(' + '|'.join(parameters) + r')\b'
    variables_in_content = re.findall(variable_pattern, content)
    
    return list(set(variables_in_content))

def extract_all_variables(line):
    # 코드에서 사용된 변수들을 추출하는 함수
    variable_pattern = r'\b\w+\b'
    variables = re.findall(variable_pattern, line)
    return list(set(variables))

def if_if_catch(java_code):
    # 메서드 파라미터 추출
    parameters, parameter_types = extract_method_parameters(java_code)

    # `if` 문 앞에 선언된 변수들 추출
    variables_before_if = extract_variables_before_if(java_code)

    # `if` 문 추출
    condition, content = extract_if_statement(java_code)
    
    if condition and content:
        # `if` 문 내부에서 사용되는 외부 변수 추출
        variables = extract_variables_in_if_statement(content, parameters)

        # 추출한 변수 타입과 이름을 파라미터로 할당
        dynamic_parameters = ', '.join([f'{var_type} {var_name}' for var_name, var_type in variables_before_if.items()])
        variable_parameters = ', '.join([f'{parameter_types[var]} {var}' for var in parameters])  # 메서드 파라미터 기반 파라미터 생성

        method_calls = []
        new_methods = []
        method_count = 1
        new_variables = []  # 새로 생성된 변수 추적

        # 기존 변수 추적
        tracked_variables = list(variables_before_if.keys()) + parameters

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # 새로운 변수 선언 여부 확인 (예: int square =)
            declaration_match = re.match(r'(int|String|double|float|char|boolean)\s+(\w+)\s*=\s*(.*);', line)
            
            # 동적으로 할당 패턴 생성
            assignment_pattern = r'(' + '|'.join(tracked_variables) + r')\s*=\s*(.*);'
            assignment_match = re.match(assignment_pattern, line)

            if declaration_match:
                var_type, var_name, expression = declaration_match.groups()
                method_name = f"generatedIfMethod{method_count}"
                method_count += 1

                # 메서드 생성시 동적으로 파라미터 할당 (정의 순서를 일치시키기 위해 변수 추가 순서 주의)
                combined_parameters = ', '.join([variable_parameters, dynamic_parameters]).strip(', ')
                # 새 메서드 생성
                new_method = f"""
    public {var_type} {method_name}({combined_parameters}) {{
        {var_type} {var_name} = {expression};
        return {var_name};
    }}
"""
                new_methods.append(new_method)

                # 메서드 호출부에 필요한 변수 순서를 맞추기 위한 처리
                method_calls.append(f"{var_type} {var_name} = {method_name}({', '.join(parameters + list(variables_before_if.keys()))});")
                
                # 추적된 변수에 추가
                new_variables.append((var_type, var_name))
                tracked_variables.append(var_name)  # 새로 선언된 변수를 추적 목록에 추가
            elif assignment_match:
                var_name, expression = assignment_match.groups()
                method_name = f"generatedIfMethod{method_count}"
                method_count += 1

                # 할당문에서 사용된 변수도 파라미터로 추가해야 함
                additional_variables = [var_name] if var_name not in tracked_variables else []
                all_parameters = ', '.join([variable_parameters, dynamic_parameters, additional_parameters]).strip(', ')
                all_variables = ', '.join(parameters + list(variables_before_if.keys()) + [var_name for _, var_name in new_variables if var_name])
                
                new_method = f"""
    public void {method_name}({all_parameters}) {{
        {var_name} = {expression};
        return {var_name};
    }}
"""
                new_methods.append(new_method)

                # 파라미터 순서를 본 메서드의 파라미터, if문 외부 변수, if문 내부 변수 순서로 조정
                method_calls.append(f"{var_name} = {method_name}({all_variables});")
                
                # 추적된 변수에 추가 (여기선 이미 존재하는 변수이므로 새로 추가하지 않음)
            else:
                # 중첩된 if/반복문 여부 확인
                if has_if_in_body(line):
                    method_name = f"generatedIfMethod{method_count}"
                    method_count += 1

                    # 중첩된 if 문이나 반복문 안에서 사용된 변수를 모두 파악
                    variables_in_line = extract_all_variables(line)

                    # 중복 파라미터를 제거하고 필요한 경우에만 추가
                    unique_variables = [var for var in variables_in_line if var not in parameters]
                    parameter_str = ', '.join([f'int {var}' for var in unique_variables])

                    # 새로운 메서드를 동적으로 생성, 변수 포함
                    combined_parameters = ', '.join([variable_parameters, dynamic_parameters, parameter_str]).strip(', ')
                    new_method = f"""
    public void {method_name}({combined_parameters}) {{
        {line.strip()}
    }}
"""
                    new_methods.append(new_method)

                    # 파라미터 순서를 본 메서드의 파라미터, if문 외부 변수, if문 내부 변수 순서로 조정
                    method_calls.append(f"{method_name}({', '.join(parameters + list(variables_before_if.keys()) + unique_variables)});")
                else:
                    # 일반적인 메서드 생성
                    method_name = f"generatedIfMethod{method_count}"
                    method_count += 1

                    # 새로 선언된 변수와 외부 변수를 파라미터에 추가
                    additional_parameters = ', '.join([f'{var_type} {var_name}' for var_type, var_name in new_variables if var_type])
                    all_parameters = ', '.join([variable_parameters, dynamic_parameters, additional_parameters]).strip(', ')
                    all_variables = ', '.join(parameters + list(variables_before_if.keys()) + [var_name for _, var_name in new_variables if var_name])

                    # 새로운 메서드 생성 (변수 순서를 정의된 순서와 맞추도록 처리)
                    new_method = f"""
    public void {method_name}({all_parameters}) {{
        {line}
    }}
"""
                    new_methods.append(new_method)

                    # 메서드 호출 시 정의된 변수 순서에 맞게 파라미터 전달 (본 메서드 파라미터 -> 외부 변수 -> 내부 변수)
                    method_calls.append(f"{method_name}({all_variables});")
        
        # 기존 `if` 문을 새로운 메서드 호출로 변경
        modified_if_block = f"if ({condition}) {{\n            " + "\n            ".join(method_calls) + "\n        }"
        
        # 기존 코드의 `if` 문을 변경된 내용으로 대체
        modified_code = re.sub(r'if\s*\(.*?\)\s*\{.*?\}', modified_if_block, java_code, flags=re.DOTALL)
        modified_code += "\n" + "\n".join(new_methods)

        return modified_code

    # `if` 문이 없을 경우 원본 코드 반환
    return java_code

# 내부 조건문 또는 반복문을 함수로 변환
def extract_internal_conditions(code_block, available_vars):
    functions = []
    modified_code_block = code_block
    match_num = 1
    
    def replace_nested_block(match):
        nonlocal match_num
        keyword = match.group(1)  # 조건문 또는 반복문 종류 (if, for, while)
        condition = match.group(2)  # 조건
        body = match.group(3).strip()  # 블록 내부 코드
        
        # 조건식에서 사용된 변수와 내부 코드에서 사용된 변수 모두 추출
        variable_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')
        condition_vars = set(variable_pattern.findall(condition))
        body_vars = set(variable_pattern.findall(body))
        all_vars = condition_vars.union(body_vars).intersection(available_vars.keys())
        
        # 각 변수의 자료형과 함께 파라미터 문자열 생성
        variables_string = ', '.join([f'{available_vars[var]} {var}' for var in all_vars])
        
        # 새 함수 이름 생성
        new_function_name = f'handleCondition{match_num}'
        match_num += 1
        
        # 새로운 함수 생성
        new_function = f'''
public void {new_function_name}({variables_string}) {{
    {keyword} ({condition}) {{
        {body}
    }}
}}
'''
        functions.append(new_function)
        
        # 함수 호출로 대체
        return f'{new_function_name}({", ".join(all_vars)});'
    
    # 내부 조건문이나 반복문을 찾아 함수로 변환
    # 조건문이나 반복문을 추출하는 정규식 (if, for, while)
    nested_pattern = re.compile(r'(if|for|while)\s*\((.*?)\)\s*\{((?:[^\{\}]|(?R))*)\}', re.MULTILINE | re.DOTALL)
    modified_code_block = nested_pattern.sub(replace_nested_block, code_block)
    
    return functions, modified_code_block

# 첫 번째 if 블록 추출 및 내부 블록 분할
def replace_first_if_block(match, available_vars):
    condition = match.group(1)  # 첫 번째 if 조건
    code_block = match.group(2).strip()  # 첫 번째 if 블록 내부 코드
    
    # 내부 조건문 또는 반복문을 함수로 분리
    new_functions, modified_code_block = extract_internal_conditions(code_block, available_vars)
    
    # 추출된 함수들 모음 (if 블록 외부에 정의)
    function_definitions = '\n'.join(new_functions)
    
    # 수정된 if 블록 반환 (원래 위치에서 함수 호출로 대체)
    modified_if_block = f'if ({condition}) {{\n    {modified_code_block}\n}}'
    
    return function_definitions, modified_if_block

# checkNumber 메서드에서 사용된 변수 목록과 자료형을 추출 (동적 파라미터 관리를 위해)
def extract_available_variables(java_code):
    declaration_pattern = re.compile(r'\b(int|float|double|String|boolean|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b')
    variable_declarations = declaration_pattern.findall(java_code)
    return {var_name: var_type for var_type, var_name in variable_declarations}

def sub(java_code):
    # 첫 번째 if 블록을 추출하는 정규식 (중첩 고려)
    if_pattern = re.compile(r'if\s*\((.*?)\)\s*\{((?:[^\{\}]|(?R))*)\}', re.MULTILINE | re.DOTALL)

    # 사용된 변수 목록을 추출 (변수명과 자료형)
    available_vars = extract_available_variables(java_code)

    # 첫 번째 if 블록을 찾아서 처리
    match = if_pattern.search(java_code)
    if match:
        function_definitions, modified_if_block = replace_first_if_block(match, available_vars)
        
        # 원래 코드에서 첫 번째 if 블록을 수정된 if 블록으로 대체
        modified_code = java_code[:match.start()] + modified_if_block + java_code[match.end():]
        
        # 추출된 함수 정의를 코드 마지막에 추가
        modified_code += '\n' + function_definitions
        
        # 최종 결과 출력
        return modified_code
    else:
        return java_code

def extract_method_by_name(java_code, method_name):
    # 중첩된 중괄호를 처리하여 메서드 전체를 추출하는 정규식 패턴
    pattern = rf'public void {method_name}\(.*?\)\s*\{{(?:[^\{{\}}]*|\{{[^\{{\}}]*\}})*\}}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        # 매칭된 메서드를 저장하고, 원래 코드에서 삭제
        extracted_method = match.group(0)  # 전체 메서드 내용을 추출
        java_code = java_code[:match.start()] + java_code[match.end():]
        return extracted_method, java_code
    return None, java_code

def reattach_method(java_code, method_code):
    # 추출한 메서드를 코드 뒤에 붙이는 함수
    return java_code.strip() + "\n\n" + method_code.strip()

#for검사
def extract_for_block_content(java_code):
    # `for` 루프와 그 내부 내용을 추출하는 정규식
    pattern = r'for\s*\((.*?)\)\s*\{(.*?)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        loop_condition = match.group(1).strip()
        loop_content = match.group(2).strip()
        return loop_condition, loop_content
    return None, None

def extract_variables_in_for_loop(loop_condition, loop_content):
    # `for` 루프의 변수 및 내용에 등장하는 변수 추출
    variable_pattern = r'(\w+)\s*[+\-*/]?='
    variables_in_condition = re.findall(variable_pattern, loop_condition)
    variables_in_content = re.findall(variable_pattern, loop_content)
    variables = set(variables_in_condition + variables_in_content)
    return list(variables)

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

def if_for_catch(java_code):
    # `for` 루프의 내용 추출
    loop_condition, loop_content = extract_for_block_content(java_code)
    
    if loop_condition and loop_content:
        # `for` 루프 내부에서 사용되는 변수 추출
        variables = extract_variables_in_for_loop(loop_condition, loop_content)
        variable_parameters = ', '.join([f'int {var}' for var in variables])  # 모든 변수를 `int`로 가정
        
        # `for` 루프 내부의 각 문장을 추출
        lines = [line.strip() for line in loop_content.splitlines() if line.strip()]
        
        method_calls = []
        new_methods = []
        method_count = 1
        
        for line in lines:
            # 새로운 메서드 이름 생성
            new_method_name = generate_random_string()

            # 수정되는 변수 확인
            modified_variable_match = re.match(r'(\w+)\s*[+\-*/]?=', line)
            if modified_variable_match:
                modified_variable = modified_variable_match.group(1).strip()
                # 새 메서드 생성 (변경된 변수 반환)
                new_method = f"""
    public int {new_method_name}({variable_parameters}) {{
        {line}
        return {modified_variable};
    }}
"""
                new_methods.append(new_method)
                method_calls.append(f"{modified_variable} = {new_method_name}({', '.join(variables)});")
            else:
                # 새 메서드 생성 (변경된 변수가 없는 경우)
                new_method = f"""
    public void {new_method_name}({variable_parameters}) {{
        {line}
    }}
"""
                new_methods.append(new_method)
                method_calls.append(f"{new_method_name}({', '.join(variables)});")
        
        # 기존 `for` 루프를 새 메서드 호출로 변경
        modified_for_loop = f"for ({loop_condition}) {{\n            " + "\n            ".join(method_calls) + "\n        }"
        
        # 새로운 메서드들 추가
        new_method_content = "\n".join(new_methods)
        
        # 기존 코드의 `for` 루프를 변경된 내용으로 대체
        modified_code = re.sub(r'for\s*\(.*?\)\s*\{.*?\}', modified_for_loop, java_code, flags=re.DOTALL)
        modified_code += f"\n{new_method_content}"
        
        return modified_code
    
    # `for` 루프가 없을 경우 원본 코드 반환
    return java_code

def if_main(java_code):
    method_data = extract_method_components(java_code)
    for method in method_data:
        sum = extract_conditionals_loops(method['if_content'])
        if sum:
            modified_code = sub(java_code)
            method_name = "handleCondition1"
            extracted_method, code_without_handle = extract_method_by_name(modified_code,method_name)
            result_after_if_catch = if_if_catch(code_without_handle)
            # 처리된 코드 뒤에 handleCondition1 메서드를 다시 붙임
            final_result = reattach_method(result_after_if_catch, extracted_method)
        else:
            final_result = if_if_catch(java_code)
        return final_result

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
    elif has_for_in_body(new_func):
        new_method_content = if_for_catch(new_func)
    elif has_if_in_body(new_func):
        new_method_content = if_main(new_func)
        print(new_method_content)
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
            print(java_content)
        # save_file_with_encoding(java_file, java_content)
        # print(f"File saved: {java_file}")

if __name__ == "__main__":
    main()