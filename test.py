import json
from typing import List, Dict, Tuple
import re
import string
import secrets

def read_and_process_json(file_path: str) -> List[Dict[str, str]]:
    result = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for item in data:
            for tainted_item in item.get('tainted', []):
                processed_item = {
                    'file_path': tainted_item.get('file_path', 'No file path provided'),
                    'method_name': tainted_item.get('method_name', 'No method name provided'),
                    'source_code': tainted_item.get('source_code', 'No source code provided')
                }
                result.append(processed_item)

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError:
        print(f"유효하지 않은 JSON 파일입니다: {file_path}")
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")
    
    return result

def extract_method_name(full_method_name: str) -> str:
    parts = full_method_name.split('.')
    if len(parts) >= 2:
        return parts[1]  # 두 번째 요소를 반환
    else:
        print(f"잘못된 method_name 형식: {full_method_name}")
        return full_method_name  # 형식이 잘못된 경우 원본 반환

def extract_method_from_source(file_path: str, method_name: str) -> tuple:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            pattern = re.compile(r'((?:public|protected|private|static|final|abstract|synchronized|)\s+)+(?:([\w\<\>\[\]]+)\s+)+' + re.escape(method_name) + r'\s*\([^\)]*\)\s*(?:\{|throws)', re.DOTALL)
            match = pattern.search(content)
            if match:
                signature = match.group(0).rstrip('{').strip()
                method_start = content.index('{', match.start())
                method_end = find_matching_brace(content, method_start)
                body = content[method_start+1:method_end].strip()
                return signature, body, match.start(), method_end + 1
            else:
                print(f"메서드를 찾을 수 없습니다: {method_name}")
                return "", "", -1, -1
    except FileNotFoundError:
        print(f"소스 파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        print(f"소스 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
    return "", "", -1, -1

def find_matching_brace(text: str, start_index: int) -> int:
    balance = 0
    for i, char in enumerate(text[start_index:], start=start_index):
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1
            if balance == 0:
                return i
    return -1  # 매칭되는 중괄호를 찾지 못한 경우

def generate_random_string(length=8):
    if length < 1:
        raise ValueError("Length must be at least 1")
    letters = string.ascii_lowercase
    letters_and_digits = string.ascii_lowercase + string.digits
    first_char = secrets.choice(letters)
    rest_chars = ''.join(secrets.choice(letters_and_digits) for _ in range(length - 1))
    return first_char + rest_chars

def extract_control_blocks(body: str) -> List[Tuple[str, str, str, List[str], List[str], bool, str]]:
    blocks = []
    
    patterns = {
        'try': r'\btry\s*\{(.*?)\}\s*catch\s*\((.*?)\)\s*\{(.*?)\}',
        'while': r'\bwhile\s*\((.*?)\)\s*\{(.*?)\}',
        'for': r'\bfor\s*\((.*?)\s*:\s*(.*?)\)\s*\{(.*?)\}',
        'do-while': r'\bdo\s*\{(.*?)\}\s*while\s*\((.*?)\);',
        'if': r'\bif\s*\((.*?)\)\s*\{(.*?)\}(?:\s*else\s*\{(.*?)\})?'
    }
    
    for structure, pattern in patterns.items():
        matches = list(re.finditer(pattern, body, re.DOTALL))
        for match in matches:
            if structure == 'try':
                try_body = match.group(1).strip()
                has_return = 'return' in try_body
                return_value = re.search(r'return\s+(.*?);', try_body)
                return_value = return_value.group(1) if return_value else None
                blocks.append((structure, try_body, f"try {{ }} catch ({match.group(2)}) {{ {match.group(3).strip()} }}", [], [], has_return, return_value))
            elif structure == 'do-while':
                do_body = match.group(1).strip()
                modified_vars = re.findall(r'(\w+)\s*=', do_body)
                has_return = 'return' in do_body
                return_value = re.search(r'return\s+(.*?);', do_body)
                return_value = return_value.group(1) if return_value else None
                blocks.append((structure, do_body, f"do {{ }} while ({match.group(2)});", modified_vars, [], has_return, return_value))
            elif structure == 'if':
                if_body = match.group(2).strip()
                else_body = match.group(3).strip() if match.group(3) else None
                modified_vars_if = re.findall(r'(\w+)\s*=', if_body)
                has_return_if = 'return' in if_body
                return_value_if = re.search(r'return\s+(.*?);', if_body)
                return_value_if = return_value_if.group(1) if return_value_if else None
                blocks.append((structure, if_body, f"if ({match.group(1)}) {{ }}", modified_vars_if, [], has_return_if, return_value_if))
                if else_body:
                    modified_vars_else = re.findall(r'(\w+)\s*=', else_body)
                    has_return_else = 'return' in else_body
                    return_value_else = re.search(r'return\s+(.*?);', else_body)
                    return_value_else = return_value_else.group(1) if return_value_else else None
                    blocks.append(('else', else_body, "else { }", modified_vars_else, [], has_return_else, return_value_else))
            elif structure == 'for':
                loop_var = match.group(1).strip().split()[-1]
                iterable = match.group(2).strip()
                for_body = match.group(3).strip()
                modified_vars = re.findall(r'(\w+)\s*=', for_body)
                has_return = 'return' in for_body
                return_value = re.search(r'return\s+(.*?);', for_body)
                return_value = return_value.group(1) if return_value else None
                blocks.append((structure, for_body, f"for ({match.group(1)} : {iterable}) {{ }}", modified_vars, [loop_var], has_return, return_value))
            else:  # while
                while_body = match.group(2).strip()
                modified_vars = re.findall(r'(\w+)\s*=', while_body)
                has_return = 'return' in while_body
                return_value = re.search(r'return\s+(.*?);', while_body)
                return_value = return_value.group(1) if return_value else None
                blocks.append((structure, while_body, f"{structure} ({match.group(1)}) {{ }}", modified_vars, [], has_return, return_value))
    
    return blocks

def create_randomized_method(signature: str, body: str) -> Tuple[str, str, str, str, List[str]]:
    random_name = generate_random_string()
    return_type = re.search(r'(?:public|protected|private|static|final|abstract|synchronized|\s)+\s*([\w\<\>\[\]]+)\s+\w+', signature)
    is_void = return_type and return_type.group(1) == 'void'
    
    new_signature = re.sub(r'(\s+[\w\<\>\[\]]+\s+)\w+\s*\(', r'\1' + random_name + '(', signature)
    
    params = re.search(r'\((.*?)\)', signature).group(1)
    param_list = [p.strip() for p in params.split(',') if p.strip()]
    param_names = [p.split()[-1] for p in param_list]
    call_params = ', '.join(param_names)
    
    if is_void:
        new_method_call = f"{random_name}({call_params});"
    else:
        new_method_call = f"return {random_name}({call_params});"
    
    extracted_blocks = extract_control_blocks(body)
    extracted_methods = []
    new_body = body
    
    for block_type, block_body, replacement, modified_vars, loop_vars, has_return, return_value in extracted_blocks:
        method_name = generate_random_string()
        if has_return:
            if return_value:
                if block_type in ['if', 'else']:
                    new_body = new_body.replace(block_body, f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});\nreturn;")
                else:
                    new_body = new_body.replace(block_body, f"return {method_name}({', '.join(param_names + loop_vars + modified_vars)});")
            else:
                if block_type in ['if', 'else']:
                    new_body = new_body.replace(block_body, f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});\nreturn;")
                else:
                    new_body = new_body.replace(block_body, f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});\nreturn;")
        else:
            if modified_vars:
                new_body = new_body.replace(block_body, f"{', '.join(modified_vars)} = {method_name}({', '.join(param_names + loop_vars + modified_vars)});")
            else:
                new_body = new_body.replace(block_body, f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});")
        
        if block_type in ['if', 'else']:
            new_body = new_body.replace(replacement, replacement.replace('{ }', f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});"))
        else:
            new_body = new_body.replace(replacement, replacement.replace('{ }', f"{method_name}({', '.join(param_names + loop_vars + modified_vars)});"))
        
        if modified_vars and not has_return:
            return_type_str = ', '.join(modified_vars)
            method_body = f"{block_body}\nreturn {return_type_str};"
        elif has_return and return_value:
            return_type_str = return_type.group(1)
            method_body = block_body
        else:
            return_type_str = "void"
            method_body = block_body
        
        method_params = ', '.join(param_list + [f"String {var}" for var in loop_vars] + [f"String {var}" for var in modified_vars])
        extracted_methods.append(f"private static {return_type_str} {method_name}({method_params}) {'throws Exception ' if block_type == 'try' else ''}{{" + f"\n    {method_body}\n" + "}")
    
    return new_signature, new_body, random_name, new_method_call, extracted_methods

def format_modified_method(original_signature: str, new_method_call: str, new_method: str, extracted_methods: List[str]) -> str:
    modified_body = f"    // 새로운 메서드 호출\n    {new_method_call}"
    result = f"{original_signature} {{\n{modified_body}\n}}\n\n{new_method}\n\n"
    for method in extracted_methods:
        result += f"{method}\n\n"
    return result

def main():
    json_file_path = 'analysis_result.json'
    processed_data = read_and_process_json(json_file_path)

    if processed_data:
        for item in processed_data:
            print(f"File Path: {item['file_path']}")
            print(f"Full Method Name: {item['method_name']}")
            
            method_name = extract_method_name(item['method_name'])
            print(f"Extracted Method Name: {method_name}")
            
            method_signature, method_body, start, end = extract_method_from_source(item['file_path'], method_name)
            if not method_signature or start == -1 or end == -1:
                print("소스 파일에서 메서드를 추출할 수 없습니다.")
                continue
            
            print(f"Original Method:\n{method_signature} {{\n{method_body}\n}}")
            
            new_signature, new_body, random_name, new_method_call, extracted_methods = create_randomized_method(method_signature, method_body)
            new_method = f"{new_signature} {{\n{new_body}\n}}"
            
            modified_method = format_modified_method(method_signature, new_method_call, new_method, extracted_methods)
            print("\n수정된 메서드 및 새로 생성된 메서드들:")
            print(modified_method)
            
            print("-" * 50)  # 구분선 출력
    else:
        print("처리된 데이터가 없습니다.")

if __name__ == "__main__":
    main()