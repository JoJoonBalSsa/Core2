import re
import random
import string

# 기존 함수들을 여기에 복사해 넣으세요

def extract_try_block_content(java_code):
    pattern = r'(public|private)\s+(\w+)\s+\w+\s*\([^)]*\)\s*\{.*?try\s*\{([\s\S]*?)\s*return\s+(.*?);'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        return_type = match.group(2)
        content = match.group(3).strip()
        return_value = match.group(4).strip()
        return content, return_value, return_type
    print(f"No match found in extract_try_block_content. Java code:\n{java_code}")
    return None, None, None

def generate_random_string(length=8):
    """특정 길이의 랜덤 문자열을 생성합니다."""
    letters = string.ascii_lowercase + string.digits  # 소문자와 숫자로 구성
    first_char = random.choice(string.ascii_lowercase)  # 첫 문자는 소문자
    remaining_chars = ''.join(random.choice(letters) for _ in range(length - 1))
    return first_char + remaining_chars
def has_try_in_body(method_body):
    return 'try' in method_body  # 단순히 문자열 포함 여부 확인

def generate_java_function(method_body, return_type, method_para):
    function_name = generate_random_string()
    java_function_code = f"""
    public {return_type} {function_name}({method_para}) {{
    {method_body}
    }}
    """
    return java_function_code, function_name

def replace_method_body(java_content, method_name, function_name, return_type, method_para):
    print(f"Replacing method body for {method_name}")
    print(f"Java content: {java_content}")
    print(f"Function name: {function_name}")
    print(f"Return type: {return_type}")
    print(f"Method parameters: {method_para}")

    method_pattern = re.compile(rf"(\b{return_type}\s+{method_name}\s*\([^)]*\)\s*{{)")
    
    match = method_pattern.search(java_content)
    if not match:
        print(f"Method {method_name} not found in the Java content.")
        return None

    start_index = match.end()
    print(f"Start index: {start_index}")

    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1
    print(f"End index: {end_index}")

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
    
    print(f"Modified body: {modified_body}")

    modified_content = (
        java_content[:start_index] + modified_body + java_content[end_index-1:]
    )
    
    print(f"Modified content: {modified_content}")
    return modified_content

def add_new_method(java_content, method_name, new_func):
    print(f"Adding new method after {method_name}")
    print(f"Java content: {java_content}")
    print(f"New function: {new_func}")

    method_pattern = re.compile(rf"\b\S+\s+{method_name}\s*\([^)]*\)\s*{{")
    
    match = method_pattern.search(java_content)
    if not match:
        print(f"Method {method_name} not found in the Java content.")
        return None
    
    start_index = match.end()
    print(f"Start index: {start_index}")

    open_braces = 1
    end_index = start_index
    while open_braces > 0 and end_index < len(java_content):
        if java_content[end_index] == '{':
            open_braces += 1
        elif java_content[end_index] == '}':
            open_braces -= 1
        end_index += 1
    print(f"End index: {end_index}")

    if has_try_in_body(new_func):
        print("Try block found in new function")
        try_content, return_value, return_type = extract_try_block_content(new_func)
        if try_content and return_value and return_type:
            print(f"Extracted try content: {try_content}")
            print(f"Extracted return value: {return_value}")
            print(f"Extracted return type: {return_type}")
            new_func_name = generate_random_string()
            print(f"Generated new function name: {new_func_name}")
            
            # Create a new function for try block content
            new_try_func = f"""
public {return_type} {new_func_name}({new_func.split('(')[1].split(')')[0]}) {{
    {try_content}
    return {return_value};
}}
"""
            print(f"New try function: {new_try_func}")

            # Modify the original new function
            modified_new_func = f"""
    public {new_func.split()[1]} {new_func.split()[2].split('(')[0]}({new_func.split('(')[1].split(')')[0]}) {{
        try {{
            return {new_func_name}({new_func.split('(')[1].split(')')[0].split()[-1]});
        }} catch (IllegalArgumentException e) {{
            return {return_value};
        }}
    }}
"""
            print(f"Modified new function: {modified_new_func}")

            new_method_content = f"\n{modified_new_func}\n{new_try_func}\n"
        else:
            print("Failed to extract try content or return value")
            new_method_content = f"\n{new_func}\n"
    else:
        print("No try block found in new function")
        new_method_content = f"\n{new_func}\n"
    
    print(f"New method content: {new_method_content}")

    modified_content = (
        java_content[:end_index] + new_method_content + java_content[end_index:]
    )
    
    print(f"Modified content: {modified_content}")
    return modified_content

# 테스트 함수들
def test_extract_try_block_content():
    test_code = """
    public boolean testMethod(String param) {
        try {
            someFunction();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
    """
    print("Test extract_try_block_content:")
    print(f"Input code:\n{test_code}")
    content, return_value, return_type = extract_try_block_content(test_code)
    print(f"Content: {content}")
    print(f"Return value: {return_value}")
    print(f"Return type: {return_type}")
    print()

def test_has_try_in_body():
    test_code_with_try = "try { someCode(); }"
    test_code_without_try = "someCode();"
    print("Test has_try_in_body:")
    print(f"With try: {has_try_in_body(test_code_with_try)}")
    print(f"Without try: {has_try_in_body(test_code_without_try)}")
    print()

def test_generate_java_function():
    test_body = "System.out.println(\"Hello\");"
    test_return_type = "void"
    test_para = "String message"
    new_func, new_func_name = generate_java_function(test_body, test_return_type, test_para)
    print("Test generate_java_function:")
    print(f"New function:\n{new_func}")
    print(f"New function name: {new_func_name}")
    print()

def test_replace_method_body():
    test_content = """
    public void testMethod(String param) {
        // Original content
    }
    """
    test_method_name = "testMethod"
    test_function_name = "newFunction"
    test_return_type = "void"
    test_para = "String param"
    modified_content = replace_method_body(test_content, test_method_name, test_function_name, test_return_type, test_para)
    print("Test replace_method_body:")
    print(f"Modified content:\n{modified_content}")
    print()

def test_add_new_method():
    test_content = """
    public class TestClass {
        public void existingMethod() {
            // Existing content
        }
    }
    """
    test_method_name = "existingMethod"
    test_new_func = """
    private boolean catchMenuError(String menu) {
        try {
            EventControlError.checkMenuError(menu);
            return false;
        } catch (IllegalArgumentException e) {
            return false;
        }
}
    """
    modified_content = add_new_method(test_content, test_method_name, test_new_func)
    print("Test add_new_method:")
    print(f"Modified content:\n{modified_content}")
    print()

# 모든 테스트 실행
def run_all_tests():
    test_extract_try_block_content()
    test_has_try_in_body()
    test_generate_java_function()
    test_replace_method_body()
    test_add_new_method()

# 테스트 실행
if __name__ == "__main__":
    run_all_tests()