import re

def has_if_in_body(method_body):
    # if 문 내부에 또 다른 if가 있는지 확인하는 함수
    pattern = r'\bif\s*\(.*?\)\s*\{'
    return bool(re.search(pattern, method_body))

def extract_if_statement(java_code):
    # `if` 문과 그 내부 내용을 추출하는 정규식
    pattern = r'if\s*\((.*?)\)\s*\{(.*?)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        condition = match.group(1).strip()
        content = match.group(2).strip()
        return condition, content
    return None, None

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

    # `if` 문 추출
    condition, content = extract_if_statement(java_code)
    
    if condition and content:
        # `if` 문 내부에서 사용되는 외부 변수 추출
        variables = extract_variables_in_if_statement(content, parameters)
        variable_parameters = ', '.join([f'{parameter_types[var]} {var}' for var in parameters])  # 변수 타입을 기반으로 파라미터 생성

        method_calls = []
        new_methods = []
        method_count = 1
        new_variables = []  # 새로 생성된 변수 추적
        external_variables = ["x"]  # 추적된 외부 변수들 (예: x)

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # 새로운 변수 선언 여부 확인 (예: int square =)
            declaration_match = re.match(r'(int|String|double|float|char|boolean)\s+(\w+)\s*=\s*(.*);', line)
            if declaration_match:
                var_type, var_name, expression = declaration_match.groups()
                method_name = f"generatedIfMethod{method_count}"
                method_count += 1
                
                # 새 메서드 생성
                new_method = f"""
    public {var_type} {method_name}({variable_parameters}, int x) {{
        {var_type} {var_name} = {expression};
        return {var_name};
    }}
"""
                new_methods.append(new_method)
                method_calls.append(f"{var_type} {var_name} = {method_name}({', '.join(parameters)}, x);")
                
                # 추적된 변수에 추가
                new_variables.append((var_type, var_name))
            else:
                # 중첩된 if/반복문 여부 확인
                if has_if_in_body(line):
                    method_name = f"generatedIfMethod{method_count}"
                    method_count += 1

                    # 중첩된 if 문이나 반복문 안에서 사용된 변수를 모두 파악
                    variables_in_line = extract_all_variables(line)

                    # 중복 파라미터를 제거하고 필요한 경우에만 추가
                    unique_variables = [var for var in variables_in_line if var not in parameters and var != 'x']
                    parameter_str = ', '.join([f'int {var}' for var in unique_variables] + ['int x'] if 'x' not in parameters else unique_variables)

                    # 새로운 메서드를 동적으로 생성, 변수 포함
                    new_method = f"""
    public void {method_name}({parameter_str}, {variable_parameters}) {{
        {line.strip()}
    }}
"""
                    new_methods.append(new_method)
                    method_calls.append(f"{method_name}({', '.join(unique_variables + parameters)});")
                else:
                    # 일반적인 메서드 생성
                    method_name = f"generatedIfMethod{method_count}"
                    method_count += 1

                    # 새로 선언된 변수와 외부 변수를 파라미터에 추가
                    additional_parameters = ', '.join([f'{var_type} {var_name}' for var_type, var_name in new_variables])
                    all_parameters = f"{variable_parameters}, {additional_parameters}".strip(', ')
                    all_variables = ', '.join([var_name for _, var_name in new_variables] + parameters)

                    # 새로운 메서드 생성
                    new_method = f"""
    public void {method_name}({all_parameters}) {{
        {line}
    }}
"""
                    new_methods.append(new_method)
                    method_calls.append(f"{method_name}({all_variables});")
        
        # 기존 `if` 문을 새로운 메서드 호출로 변경
        modified_if_block = f"if ({condition}) {{\n            " + "\n            ".join(method_calls) + "\n        }"
        
        # 기존 코드의 `if` 문을 변경된 내용으로 대체
        modified_code = re.sub(r'if\s*\(.*?\)\s*\{.*?\}', modified_if_block, java_code, flags=re.DOTALL)
        modified_code += "\n" + "\n".join(new_methods)
        
        return modified_code

    # `if` 문이 없을 경우 원본 코드 반환
    return java_code

# 테스트 코드
def test_if_if_catch():
    java_code = '''
    public void checkNumber(int number) {
        System.out.println("First");
        System.out.println("second");
        int x = 3;
        if (number > 0) {
            System.out.println("Positive");
            int square = number * number;
            System.out.println("Square: " + square);
            square = square + x;
        }
        System.out.println("First");
        System.out.println("second");
    }
    '''
    
    result = if_if_catch(java_code)
    print("Modified Code:\n", result)

# 실행
test_if_if_catch()
