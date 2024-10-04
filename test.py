import re

def extract_if_statement(java_code):
    # `if` 문과 그 내부 내용을 추출하는 정규식
    pattern = r'if\s*\((.*?)\)\s*\{(.*?)\}'
    match = re.search(pattern, java_code, re.DOTALL)
    if match:
        condition = match.group(1).strip()
        content = match.group(2).strip()
        return condition, content
    return None, None

def if_if_catch(java_code):
    # `if` 문 추출
    condition, content = extract_if_statement(java_code)
    
    if condition and content:
        # `if` 문 내부의 각 문장을 추출
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        method_name = "generatedIfMethod"
        
        # 새 메서드 생성
        new_method = f"""
    public void {method_name}() {{
        if ({condition}) {{
            {' '.join(lines)}
        }}
    }}
"""
        # 원래 코드의 `if` 문을 변경된 내용으로 대체
        modified_code = re.sub(r'if\s*\(.*?\)\s*\{.*?\}', f'{method_name}();', java_code, flags=re.DOTALL)
        modified_code += f"\n{new_method}"
        
        return modified_code

    # `if` 문이 없을 경우 원본 코드 반환
    return java_code

# 테스트 코드
def test_if_if_catch():
    java_code = '''
    public void checkNumber(int number) {
        if (number > 0) {
            System.out.println("Positive");
            int square = number * number;
            System.out.println("Square: " + square);
        }
    }
    '''
    
    result = if_if_catch(java_code)
    print("Modified Code:\n", result)

# 실행
test_if_if_catch()