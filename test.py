import re

def extract_modified_variable(while_content):
    # 변경되는 변수 찾는 정규식 (예: x = 10, x += 10 등)
    modified_variable_pattern = r'(\w+)\s*(?:[+\-*/]?=)\s*[^;]+;'
    matches = re.findall(modified_variable_pattern, while_content)
    return matches

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
                new_func_name = f"generatedFunction{method_count}"
                method_count += 1
                
                # Generate the new method with modified parameters and return type
                remaining_parameters = ', '.join([param for param in param_list if param.split()[-1] != variable_to_modify])
                if remaining_parameters:
                    new_method = f"""
    public {variable_type} {new_func_name}({variable_type} {variable_to_modify}, {remaining_parameters}) {{
        {line}
        return {variable_to_modify};  // Return modified variable
    }}
"""
                    method_calls.append(f"{variable_to_modify} = {new_func_name}({variable_to_modify}, {', '.join([param.split()[-1] for param in param_list if param.split()[-1] != variable_to_modify])});")
                else:
                    new_method = f"""
    public {variable_type} {new_func_name}({variable_type} {variable_to_modify}) {{
        {line}
        return {variable_to_modify};  // Return modified variable
    }}
"""
                    method_calls.append(f"{variable_to_modify} = {new_func_name}({variable_to_modify});")
            else:
                # Generate void method if no modified variable
                new_func_name = f"generatedFunction{method_count}"
                method_count += 1
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
        {while_start} {{
            {method_calls_str}
        }}
        {after_while_code}
    }}
"""
        new_method_content = f"\n{modified_new_func}\n" + "\n".join(new_methods) + "\n"
    else:
        new_method_content = f"\n{new_func}\n"
    
    return new_method_content


def test_if_while_catch():
    # 테스트 케이스 1: while 안에서 변수가 변경되는 경우
    java_code_1 = '''
    public void exampleMethod(int x, String name) {
        int y = 0;

        while (catchDateError(date)) {
            x += 10;
            System.out.println(name);
            y = 5;
        }

        System.out.println("End of method");
    }
    '''

    # 테스트 케이스 2: while 안에서 변수가 변경되지 않는 경우
    java_code_2 = '''
    public void anotherMethod(int i) {
        while (i < 10) {
            System.out.println(i);
        }
    }
    '''

    # 테스트 케이스 3: while 안에 변경되는 변수가 있고 파라미터로 전달해야 하는 경우
    java_code_3 = '''
    public void processData(int count) {
        while (count > 0) {
            count -= 1;
            System.out.println("Processing...");
        }
        System.out.println("hello");
    }
    '''

    java_code_4 = '''
    public void inputMenu() {
        EventView.orgerGuideMessage();

        String menu = Console.readLine();
        while (catchMenuError(menu)) {
            EventModel.eraseOrderedMenu();
            EventView.tryAgainMessage();
            menu = Console.readLine();
        }

        EventView.printOrderedMenu();
    }
'''
    # 테스트 실행 및 결과 출력
    print("Test Case 1:")
    result_1 = if_while_catch(java_code_1)
    print(result_1)
    print("\n")

    print("Test Case 2:")
    result_2 = if_while_catch(java_code_2)
    print(result_2)
    print("\n")

    print("Test Case 3:")
    result_3 = if_while_catch(java_code_3)
    print(result_3)
    print("\n")

    print("Test Case 4:")
    result_4 = if_while_catch(java_code_4)
    print(result_4)
    print("\n")

# 테스트 실행
test_if_while_catch()