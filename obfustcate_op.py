import javalang
import os
import json

class obfuscate_Op:
    def __init__(self,java_folder):
        self.ob_json = self.load_obfuscation_map('C:/Users/조준형/Desktop/S개발자_프로젝트/obfuscate_if_for/culDB.json')
        self.files = self.parse_java_files(java_folder)
        self.__extract_conditions(self.files)#조건문,반복문 식별 후 연산자 추출


    def load_obfuscation_map(self,json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            ob_json = json.load(file)
        return ob_json

    def obfuscate_expression(self,condition):

        # JSON 파일에서 정의한 연산자 변환 적용
        for original, obfuscated in self.ob_json.items():
            condition = condition.replace(original, obfuscated)

        return condition
    
    def insert_ob_op(self,file_path,code, conditions):
        lines = code.split('\n')

        for condition_type, condition, position in conditions:

            if condition_type == "If": # if 문 후에 중괄호가 올수도있고 안올수도있음 중괄호가 어디에 위치해 있는지도 알아야함
                line = lines[position[0] - 1]
                updated_line = self.obfuscate_expression(condition)
                lines[position[0] - 1] = line.replace(condition,updated_line)


        code = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)



            

    def __extract_conditions(self,files):
        for file_path, tree , code in files:
            conditions = self.extract_conditions(tree)
            print(f'File: {file_path}')
            self.insert_ob_op(file_path,code,conditions)
                #print(f'{condition_type} statement at line {position.line}, column {position.column}:')
                #print(f'Condition: {condition}')
                #여기다가 난독화 후 코드 삽입 부분 추가
            #print()

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
