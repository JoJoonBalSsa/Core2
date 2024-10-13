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
                print(variable_parameters)
                print(dynamic_parameters)
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
