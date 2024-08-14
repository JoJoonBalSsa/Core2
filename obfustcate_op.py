import javalang
import os
import json
import re

class obfuscate_Op:
    def __init__(self,java_folder): # 연산자 우선순위 정하고, load_obfucation(난독화 DB 불러오기) , __extract_conditions (조건 추출)
        self.file = None
        self.OPERATOR_PRECEDENCE = {
    '~': 14,  
    '!': 14, 
    '++': 14,
    '*': 13, '/': 13, '%': 13,
    '+': 12, '-': 12,
    '<<': 11, '>>': 11, '>>>': 11,
    '<': 10, '>': 10, '<=': 10, '>=': 10,
    '==': 9, '!=': 9,
    '&': 8,
    '^': 7,
    '|': 6,
    '&&': 5,
    '||': 4,
    '?:': 3,
    '=': 2, '+=': 2, '-=': 2, '*=': 2, '/=': 2, '%=': 2,
    '&=': 2, '|=': 2, '^=': 2,
    '<<=': 2, '>>=': 2, '>>>=': 2,
    '.': 1,
    '()': 1,
    '[]': 1,
    '::': 1
}
            
        self.ob_json = self.load_obfuscation_map('C:/Users/조준형/Desktop/S개발자_프로젝트/obfuscate_if_for/culDB.json')
        self.files = self.parse_java_files(java_folder)
        self.__extract_conditions(self.files) #조건문,반복문 식별 후 연산자 추출


    def load_obfuscation_map(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            ob_json = json.load(file)
        return ob_json
    
    def preprocess_expression(self, expression):
        expression = re.sub(r'([a-zA-Z_]\w*)\s*\(([^()]*?)\)', r'\1(\2)', expression)
        expression = re.sub(r'(?<!\d)0(?!\d)', '00', expression)
        return expression
    


    def remove_whitespace(self,text):
        return ''.join(text.split())

    def replace_expression_without_whitespace(self,original_line, expression, new_expression):
        # 공백을 제거한 후 비교
        clean_line = self.remove_whitespace(original_line)
        clean_expression = self.remove_whitespace(expression)


        if clean_expression in clean_line:
            # 공백을 포함한 원래 라인에서 대체
            return clean_line.replace(clean_expression, new_expression).replace("else","else ")
        return clean_line
    
    def obfuscate_expression(self, expression):
        if not expression or expression.isspace():
            return expression

        # Preprocess the expression before tokenizing
        preprocessed_expr = self.preprocess_expression(expression)

        try:
            tokens = list(javalang.tokenizer.tokenize(preprocessed_expr))
        except Exception as e:
            print(f"error tokenizing expression '{preprocessed_expr}': {e}")
            return expression 

        operators = []
        operands = []

        current_operand = ""
        last_position = None
        first_operand_type = None
        first_operand_name = None

        for token in tokens:
            if isinstance(token, javalang.tokenizer.Keyword):
                first_operand_type = token.value  # 첫 번째 변수의 타입 저장
                current_operand = ""  # 타입을 따로 저장하고 초기화
                last_position = token.position

            elif isinstance(token, javalang.tokenizer.Operator):
                if current_operand:
                    if not first_operand_name:
                        first_operand_name = current_operand.strip()  # 첫 번째 변수 이름 저장
                    operands.append((current_operand.strip(), last_position))
                    current_operand = ""
                operators.append((token.value, token.position))

            elif isinstance(token, (javalang.tokenizer.Identifier, javalang.tokenizer.Literal)):
                if current_operand:
                    current_operand += token.value
                else:
                    current_operand = token.value
                last_position = token.position

            elif token.value == '.':
                current_operand += '.'

            elif token.value in ('(', ')'):
                current_operand += token.value

        if current_operand:
            if not first_operand_name:
                first_operand_name = current_operand.strip()  # 첫 번째 변수 이름 저장
            operands.append((current_operand.strip(), last_position))

        obfuscated_expr = self.recursive_obfuscate(operators, operands)

        # 첫 번째 변수에만 타입을 붙임 (선언 부분)
        if first_operand_type and first_operand_name:
            obfuscated_expr = obfuscated_expr.replace(first_operand_name, f'{first_operand_type} {first_operand_name}', 1)

        return obfuscated_expr

    def recursive_obfuscate(self, operators, operands):
        if not operators:
            return operands[0][0]

        try:
            max_precedence = max(self.OPERATOR_PRECEDENCE[op[0]] for op in operators)
        except ValueError:            
            return operands[0][0]


        try:
            index = next(i for i, op in enumerate(operators) if self.OPERATOR_PRECEDENCE[op[0]] == max_precedence)
        except StopIteration:
            return operands[0][0]

        left_operand = operands[index][0]
        operator = operators[index][0]
        right_operand = operands[index + 1][0]

        obfuscated_expression = self.ob_json[operator].format(a=left_operand, b=right_operand)

        new_operands = operands[:index] + [(obfuscated_expression, operands[index][1])] + operands[index + 2:]
        new_operators = operators[:index] + operators[index + 1:]

        return self.recursive_obfuscate(new_operators, new_operands)


    def extract_for_parts(self, for_expression):
        # for 문 내에서 세미콜론(;)을 기준으로 초기화, 조건, 증감 부분을 추출
        parts = for_expression.split(';')
        if len(parts) == 3:
            init_part = parts[0].strip()
            condition_part = parts[1].strip()
            increment_part = parts[2].strip()
            return init_part, condition_part, increment_part
        else:
            raise ValueError("Invalid for loop expression")
    
    def insert_ob_op(self,file_path,code, conditions):
        lines = code.split('\n')

        for condition_type, condition, position in conditions:

            if condition_type == "If" or condition_type == "While":
                line = lines[position[0] - 1]
                self.file = file_path # 디버깅
                updated_line = self.obfuscate_expression(condition)
                lines[position[0] - 1] = self.replace_expression_without_whitespace(line,condition,updated_line)
            
            elif condition_type == "For":
                line = lines[position[0] - 1]
                self.file = file_path  # 디버깅용

                # For 문에서 초기화, 조건, 증감 부분을 추출
                init_part, condition_part, increment_part = self.extract_for_parts(condition)

                # 각 부분을 난독화
                obfuscated_init = self.obfuscate_expression(init_part)
                obfuscated_condition = self.obfuscate_expression(condition_part)
                obfuscated_increment = increment_part #self.obfuscate_expression(increment_part) #일단 후위 전위 연산 넣을때까진 주석처리

                # 난독화된 부분들을 결합하여 최종 for 문 구성
                updated_line = f"{obfuscated_init}; {obfuscated_condition}; {obfuscated_increment}"

                lines[position[0] - 1] = self.replace_expression_without_whitespace(line, condition, updated_line)

        code = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)



            

    def __extract_conditions(self,files):
        for file_path, tree , code in files:
            conditions = self.extract_conditions(tree) #여기서 IF,FOR 등등 식별
            self.insert_ob_op(file_path,code,conditions) #난독화 코드 삽입

    def parse_java_files(self,folder_path):
        java_files = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        source_code = file.read()
                    tree = javalang.parse.parse(source_code)
                    java_files.append((file_path, tree,source_code))
        return java_files
    
    def expression_to_string(self, expr , parent = None):
        if isinstance(expr, javalang.tree.Literal):
            return expr.value
        
        elif isinstance(expr, javalang.tree.BinaryOperation):
            left = self.expression_to_string(expr.operandl, expr)
            right = self.expression_to_string(expr.operandr, expr)
            if parent and isinstance(parent, javalang.tree.BinaryOperation):
                return f'{left} {expr.operator} {right}'
            return f'{left} {expr.operator} {right}'
        
        elif isinstance(expr, javalang.tree.MemberReference):
            qualifier = self.expression_to_string(expr.qualifier) if expr.qualifier else ''
            member = expr.member
            if expr.postfix_operators: # 후위 연산자 확인
                member += expr.postfix_operators[0]
            elif expr.prefix_operators: # 전위 연산자 확인
                member = expr.prefix_operators[0] + member

            return f'{qualifier}.{member}' if qualifier else member
        
        elif isinstance(expr, javalang.tree.MethodInvocation):
            args = ', '.join(self.expression_to_string(arg) for arg in expr.arguments)
            qualifier = self.expression_to_string(expr.qualifier) if expr.qualifier else ''
            return f'{qualifier}.{expr.member}({args})' if qualifier else f'{expr.member}({args})'
        elif isinstance(expr, javalang.tree.VariableDeclarator):
            init = self.expression_to_string(expr.initializer) if expr.initializer else ''
            return f'{expr.name} = {init}' if init else expr.name
        elif isinstance(expr, javalang.tree.VariableDeclaration):
            type_str = expr.type.name
            declarators = ', '.join(self.expression_to_string(decl) for decl in expr.declarators)
            return f'{type_str} {declarators}'
        elif isinstance(expr, javalang.tree.Assignment):
            print(expr)
            return f'{self.expression_to_string(expr.expressionl)} {expr.operator} {self.expression_to_string(expr.value)}'
        elif isinstance(expr, javalang.tree.EnhancedForControl):
            return f'{expr.var.name} : {self.expression_to_string(expr.iterable)}'
        elif isinstance(expr, javalang.tree.ReferenceType):
            return expr.name
        elif isinstance(expr, javalang.tree.TypeArgument):
            return expr.type.name
        elif isinstance(expr, javalang.tree.Type):
            return expr.name
        elif isinstance(expr, javalang.tree.ArraySelector):
            return f'{self.expression_to_string(expr.index)}'
        elif isinstance(expr, javalang.tree.FieldDeclaration):
            return ', '.join(self.expression_to_string(decl) for decl in expr.declarators)
        elif isinstance(expr, javalang.tree.LocalVariableDeclaration):
            return ', '.join(self.expression_to_string(decl) for decl in expr.declarators)
        elif isinstance(expr, javalang.tree.StatementExpression):
            return self.expression_to_string(expr.expression)
        elif isinstance(expr, javalang.tree.FormalParameter):
            return expr.name
        elif isinstance(expr, javalang.tree.This):
            return "this"
        elif isinstance(expr, javalang.tree.SuperMethodInvocation):
            return f"super.{expr.member}({', '.join(self.expression_to_string(arg) for arg in expr.arguments)})"
        else:
            return str(expr)


    def extract_conditions(self,tree):
        conditions = []
        for path, node in tree:
            if isinstance(node, javalang.tree.IfStatement):
                condition_str = self.expression_to_string(node.condition)
                conditions.append(('If', condition_str, node.position))
            elif isinstance(node, javalang.tree.WhileStatement):
                condition_str = self.expression_to_string(node.condition)
                conditions.append(('While', condition_str, node.position))
            elif isinstance(node, javalang.tree.ForStatement):
                if isinstance(node.control, javalang.tree.ForControl):
                    #init_str = ', '.join(self.expression_to_string(i) for i in node.control.init)
                    init_str = (self.expression_to_string(node.control.init))
                    condition_str = self.expression_to_string(node.control.condition) if node.control.condition else ''
                    update_str = ', '.join(self.expression_to_string(i) for i in node.control.update)
                    for_control_str = f'{init_str}; {condition_str}; {update_str}'
                    conditions.append(('For', for_control_str, node.position))
                elif isinstance(node.control, javalang.tree.EnhancedForControl):
                    iterable_str = self.expression_to_string(node.control.iterable)
                    var_decl_str = self.expression_to_string(node.control.var)
                    conditions.append(('EnhancedFor', f'{var_decl_str} : {iterable_str}', node.position))
            elif isinstance(node, javalang.tree.DoStatement):
                condition_str = self.expression_to_string(node.condition)
                conditions.append(('DoWhile', condition_str, node.position))
        return conditions
