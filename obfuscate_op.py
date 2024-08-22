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
        # 괄호 안의 내용을 먼저 처리
        expression = self.apply_operator_priority(expression)

        # 임시 기호를 원래의 난독화된 표현으로 대체
        for key, value in sorted(self.obfuscation_map.items(), reverse=True):
            expression = expression.replace(key, f"{value}")  # 괄호를 추가하지 않고 원래 표현으로 대체

        return expression

    def apply_operator_priority(self, expression):
        while '(' in expression:
            expression = re.sub(r'\(([^()]+)\)', lambda x: self.apply_operator_priority(x.group(1)), expression)

        # 연산자 우선순위에 따라 처리
        for operator_pattern in self.ob_json.keys():
            pattern = re.compile(rf'(\([^()]+\)|\b-?\w+\b|-?\d+)\s*({re.escape(operator_pattern)})\s*(\([^()]+\)|\b-?\w+\b|-?\d+)')




            expression = ''.join(expression)
            match = pattern.search(expression)
            while match:
                operand1 = match.group(1)
                operator = match.group(2)
                operand2 = match.group(3)

                # 디버깅용 출력
                #print(f"Identified operator: {operator} between '{operand1}' and '{operand2}'")

                # 식별된 연산자를 적용하여 난독화된 표현으로 변경
                obfuscated = self.ob_json[operator].format(a=operand1, b=operand2)

                # 임시 기호로 대체, 괄호를 제외한 부분만 대체
                temp_key = f"__OBFUSCATED_{self.counter}__"
                self.obfuscation_map[temp_key] = f"{obfuscated}"
                expression = expression[:match.start()] + temp_key + expression[match.end():]
                self.counter += 1

                # 다시 연산자를 찾아서 처리
                match = pattern.search(expression)

        return expression