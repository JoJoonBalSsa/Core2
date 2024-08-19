import re
import json


class obfuscate_Op:
    def __init__(self):
        self.ob_json = self.load_obfuscation_map('C:/Users/조준형/Desktop/S개발자_프로젝트/obfuscate_if_for/culDB.json')

        # 연산자 우선순위 리스트 (우선순위 높은 것부터 나열)
        self.operator_priority = [
            r'\*\*',  # 거듭제곱 연산자 (Python 스타일)
            r'\*', r'/', r'%',  # 곱셈, 나눗셈, 나머지
            r'\+', r'-',  # 덧셈, 뺄셈
            r'<<', r'>>', r'>>>',  # 시프트 연산자
            r'<', r'<=', r'>', r'>=', r'instanceof',  # 비교 연산자
            r'==', r'!=',  # 동등 비교 연산자
            r'&',  # 비트 AND
            r'\^',  # 비트 XOR
            r'\|',  # 비트 OR
            r'&&',  # 논리 AND
            r'\|\|',  # 논리 OR
            r'\?', r'\:',  # 삼항 연산자
            r'=', r'\+=', r'-=', r'\*=', r'/=', r'%=', r'<<=', r'>>=', r'>>>=', r'&=', r'\^=', r'\|=',  # 대입 연산자
        ]

        self.obfuscation_map = {}  # 난독화된 부분을 임시 저장할 맵

        self.counter = 0  # 난독화 넘버링에 사용


    def load_obfuscation_map(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            ob_json = json.load(file)
        return ob_json
    
    def obfuscate_expression(self, expression):
        #print(f"Starting obfuscation for expression: {expression}")


        # 괄호 안의 내용부터 재귀적으로 처리
        expression = self.process_parentheses(expression)

        # 모든 난독화가 끝난 후  임시 기호를 원래의 난독화된 표현으로 대체 (괄호 포함)
        for key, value in sorted(self.obfuscation_map.items(), reverse=True):
            expression = expression.replace(key, f"({value})")

        return expression

    def process_parentheses(self, expression):
        # 괄호 안의 내용을 재귀적으로 먼저 처리
        def replace_inside_parentheses(match):
            inside_expression = match.group(1)
            obfuscated_inside = self.obfuscate_expression(inside_expression)
            temp_key = f"__OBFUSCATED_{self.counter}__"
            self.obfuscation_map[temp_key] = obfuscated_inside
            self.counter += 1
            return temp_key

        # 가장 안쪽 괄호부터 처리
        while '(' in expression:
            expression = re.sub(r'\(([^()]+)\)', replace_inside_parentheses, expression)

        # 연산자 처리
        for operator_pattern in self.operator_priority:
            expression = self.apply_operator_priority(expression, operator_pattern)

        return expression

    def apply_operator_priority(self, expression, operator_pattern):
        # 이미 난독화된 표현식을 임시 기호로 대체하면서 연산 적용
        pattern = re.compile(rf'(\w+\s+\w+|\b\w+\b|\d+|\(.+?\))\s*({operator_pattern})\s*(\w+\s+\w+|\b\w+\b|\d+|\(.+?\))')
        match = pattern.search(expression)
        while match:
            operand1 = match.group(1)
            operator = match.group(2)
            operand2 = match.group(3)

            #print(f"Identified operands: '{operand1}' and '{operand2}' with operator: '{operator}'")

            # 식별된 연산자를 앞에 붙여서 난독화된 표현으로 변경
            obfuscated = self.ob_json[operator].format(a=operand1, b=operand2)
            #print(f"Obfuscating to: {obfuscated}")

            # 임시 기호로 대체
            temp_key = f"__OBFUSCATED_{self.counter}__"
            self.obfuscation_map[temp_key] = obfuscated
            expression = expression[:match.start()] + temp_key + expression[match.end():]
            self.counter += 1
            #print(f"Updated expression with temporary key: {expression}")

            # 다시 연산자를 찾아서 처리
            match = pattern.search(expression)
        return expression