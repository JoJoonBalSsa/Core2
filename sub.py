import os
import javalang
import random
import string

def read_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_java_code(code):
    tree = javalang.parse.parse(code)
    return tree

def generate_random_name(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def split_method(method_node, class_node):
    statements = method_node.body
    if statements and len(statements) > 2:
        # 메서드 본문을 두 부분으로 분할
        mid = len(statements) // 2
        first_part = statements[:mid]
        second_part = statements[mid:]
        
        # 새로운 메서드 이름 생성
        new_method_name = generate_random_name()
        
        # 새로운 메서드 생성
        new_method = javalang.tree.MethodDeclaration(
            name=new_method_name,
            modifiers={'private'},
            return_type=method_node.return_type,
            parameters=method_node.parameters,
            body=second_part
        )
        
        # 기존 메서드 본문 업데이트
        method_node.body = first_part + [
            javalang.tree.StatementExpression(
                expression=javalang.tree.MethodInvocation(
                    name=new_method_name,
                    arguments=[param.name for param in method_node.parameters]
                )
            )
        ]
        
        # 클래스에 새로운 메서드 추가
        class_node.body.append(new_method)

def obfuscate_methods(tree):
    for type_decl in tree.types:
        if isinstance(type_decl, javalang.tree.ClassDeclaration):
            for member in type_decl.body:
                if isinstance(member, javalang.tree.MethodDeclaration):
                    split_method(member, type_decl)

def generate_code_from_ast(tree):
    code_lines = []

    for type_decl in tree.types:
        code_lines.append(f'public class {type_decl.name} ' + '{')
        for member in type_decl.body:
            if isinstance(member, javalang.tree.FieldDeclaration):
                code_lines.append(generate_field_code(member))
            elif isinstance(member, javalang.tree.MethodDeclaration):
                code_lines.append(generate_method_code(member))
        code_lines.append('}')
    
    return '\n'.join(code_lines)

def generate_field_code(field):
    type_str = field.type.name
    vars_str = ', '.join([var.name for var in field.declarators])
    return f'    {type_str} {vars_str};'

def generate_method_code(method):
    modifiers = ' '.join(method.modifiers)
    return_type = method.return_type.name if method.return_type else 'void'
    params = ', '.join([f'{param.type.name} {param.name}' for param in method.parameters])
    body = generate_method_body(method.body)
    return f'    {modifiers} {return_type} {method.name}({params}) ' + '{\n' + body + '\n    }'

def generate_method_body(statements):
    body_lines = []
    for stmt in statements:
        if isinstance(stmt, javalang.tree.StatementExpression):
            expr = stmt.expression
            if isinstance(expr, javalang.tree.MethodInvocation):
                args = ', '.join(expr.arguments)
                body_lines.append(f'        {expr.name}({args});')
        elif isinstance(stmt, javalang.tree.LocalVariableDeclaration):
            var_type = stmt.type.name
            for decl in stmt.declarators:
                body_lines.append(f'        {var_type} {decl.name} = {decl.initializer.value};')
    return '\n'.join(body_lines)

def obfuscate_java_file(input_path, output_path):
    code = read_java_file(input_path)
    tree = parse_java_code(code)
    obfuscate_methods(tree)
    obfuscated_code = generate_code_from_ast(tree)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)
    print(f'난독화된 코드가 {output_path}에 저장되었습니다.')

def obfuscate_all_java_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(root, f'obfuscated_{file}')
                obfuscate_java_file(input_path, output_path)

if __name__ == '__main__':
    folder_path = 'C:/Users/sangbin/OneDrive/바탕 화면/vscode4/java-christmas-6-scienceNH/src/main'  # 여기서 폴더 경로를 지정하세요
    obfuscate_all_java_files_in_folder(folder_path)
