import javalang
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from keyObfuscate import KeyObfuscate


class StringObfuscate:
    def __init__(self, class_name, class_position):
        self.class_name = class_name
        self.class_position = class_position

        self.aes_key = os.urandom(16)
        self.enc_aes_key = os.urandom(8)

        self.encrypted_aes_key = None
        self.lines = None
        self.count = 0 # 복호화 코드 삽입할 소스코드
        self.random = 1 # 랜덤으로 소스코드 정하기
        self.decryptor_package = None
        self.decryptor_class = None
        


    def split_source_code(self, source_code):
        self.lines = source_code.split('\n')


    def encrypt_string_literals(self, string_literals): # 암호화
        encrypted_literals = [self.encrypt_string(literal, self.aes_key) for literal, _ in string_literals]
        
        return encrypted_literals


    def encrypt_string(self, plain_text, key):
        cipher = AES.new(key, AES.MODE_ECB)
        padded_text = pad(plain_text.encode('utf-8'), AES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted_text).decode('utf-8')
    

    def replace_string_literals(self, string_literals):
        string_literals_sorted = sorted(string_literals, key=lambda x: (x[1][0], -x[1][1]))  # 라인 오른쪽부터 문자열 변환
        for index, (literal, position) in enumerate(string_literals_sorted):
            line_index = position[0] - 1
            column_index = position[1] - 1
            line = self.lines[line_index]
            end_column_index = column_index + len(literal)
            new_line = line[:column_index] + f'STRING_LITERALS_{self.class_name.upper()}[{index}]' + line[end_column_index:]
            self.lines[line_index] = new_line
            self.lines = '\n'.join(self.lines)


    def insert_encrypted_string_array(self, encrypted_literals):
        # 문자열이 원래 있던 자리를 배열참조로 바꿈
        # 지금은 STRING_LITERALS_{class 이름} 인데 바꿔도됨
        array_declaration = f'public static final String[] STRING_LITERALS_{self.class_name.upper()} = {{' + ','.join(f'"{literal}"' for literal in encrypted_literals) + '\n};\n'
        
        self.lines.insert(self.class_position, array_declaration)
        reflection = 'import java.lang.reflect.Method;'
        if reflection not in self.lines:
                self.lines.insert(1, reflection)

        # 복호화 코드 삽입
        # TO-DO : 클래스 이름 동적할당 필요?
        decryption_code = f"""
            static{{try {{Class<?> decryptorClass1 = Class.forName("christmas.KeyDecrypt");
            Method decryptMethod1 = decryptorClass1.getMethod("keyDecrypt", String.class, String.class);
            Class<?> decryptorClass2 = Class.forName("christmas.StringDecrypt");
            Method decryptMethod2 = decryptorClass2.getMethod("decryptString", String.class, byte[].class);
            for (int i = 0; i < STRING_LITERALS_{self.class_name.upper()}.length; i++) 
            {{STRING_LITERALS_{self.class_name.upper()}[i] = 
            (String) decryptMethod2.invoke(null, STRING_LITERALS_{self.class_name.upper()}[i], 
            (byte[]) decryptMethod1.invoke(null,ENC_ENCRYPTION_KEY_{self.class_name.upper()},
            ENCRYPTION_KEY_{self.class_name.upper()})); 
            }}}} catch (Exception e) {{}}}}
        """

        self.lines.insert(self.class_position + 2, decryption_code)
        self.lines = '\n'.join(self.lines)

        # decryption_code = f"""
        # static {{
        #     for (int i = 0; i < STRING_LITERALS_{class_name.upper()}.length; i++) {{
        #         STRING_LITERALS_{class_name.upper()}[i] = new String(AES.decrypt(STRING_LITERALS_{class_name.upper()}[i], ENCRYPTION_KEY_{class_name.upper()}.getBytes()));
        #     }}
        # }}
        # """
    

    def encrypt_aes_key(self):
        ko = KeyObfuscate(self.aes_key, self.enc_aes_key)
        self.encrypted_aes_key = ko.enc_aes_key


    def insert_encryption_key(self): # 키를 난독화하여 문자열에 추가하는 함수
        key_declaration = f'private static final String ENC_ENCRYPTION_KEY_{self.class_name.upper()} = "{base64.b64encode(self.encrypted_aes_key).decode('utf-8').replace("=","")}";\n'
        key_declaration += f'private static final String ENCRYPTION_KEY_{self.class_name.upper()} = "{base64.b64encode(self.enc_aes_key).decode('utf-8').replace("=","")}";\n'

        self.lines.insert(self.class_position + 1, key_declaration)
        self.lines = '\n'.join(self.lines)
    

    def insert_decryptor_class(self, decryptor_class_path, key_decryptor_class_path):
        with open(decryptor_class_path, 'r', encoding='utf-8') as file:
            decryptor_code = file.read()
        with open(key_decryptor_class_path,'r',encoding='utf-8') as file:
            key_decryptor_code = file.read()

        decryptor_code = decryptor_code.split('\n')
        decryptor_code = [line for line in decryptor_code if not line.startswith('import')]
        decryptor_code = '\n'.join(decryptor_code)
        key_decryptor_code = key_decryptor_code.split('\n')
        key_decryptor_code = [line for line in key_decryptor_code if not line.startswith('import')]
        key_decryptor_code = '\n'.join(key_decryptor_code)

        # Import 문 추가    
        import_statements = [
            'import javax.crypto.Cipher;',
            'import javax.crypto.KeyGenerator;',
            'import javax.crypto.SecretKey;',
            'import javax.crypto.spec.SecretKeySpec;',
            'import java.util.Base64;',
            'import java.lang.reflect.Method;'
            'import java.security.MessageDigest;'
            'import java.security.NoSuchAlgorithmException;',
            'import java.util.ArrayList;',
            'import java.util.Arrays;',
            'import java.util.Base64;',
            'import java.util.List;'
        ]
        for import_statement in import_statements:
            if import_statement not in self.lines:
                self.lines.insert(1, import_statement)

        # AESDecryptor 클래스 추가
        self.lines.append(decryptor_code)
        self.lines.append(key_decryptor_code)

        self.lines = '\n'.join(self.lines)
    
    #   with open(decryptor_class_path, 'r', encoding='utf-8') as file:
    #       decryptor_code = file.read()        
    #   lines = source_code.split('\n')
    #   lines.append(decryptor_code)
    #   return '\n'.join(lines)
    



def get_package_name(tree): 
    #패키지 이름 알아내기(for reflection)
    for path, node in tree:
        if isinstance(node, javalang.tree.PackageDeclaration):
            return node.name
    return None
    

def parse_java_files(folder_path): # 소스코드 => AST tree
        java_files = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        source_code = file.read()
                    tree = javalang.parse.parse(source_code)
                    java_files.append((file_path, tree, source_code))
        return java_files


def extract_string_literals(tree): # AST 에서 문자열 찾아내고 문자열 값과 위치 저장
        string_literals = []
        for path, node in tree:
            if isinstance(node, javalang.tree.Literal) and isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
                string_literals.append((node.value, node.position))
        return string_literals


def execute(java_files,decryptor_class_path,key_cecryptor_class_path):
    for file_path, tree, source_code in java_files:
        class_declarations = []

        # encrypt_str.decryptor_package = get_package_name(tree)
        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration): #클래스 별로 문자열을 추출할것이기 때문에 클래스 정의 위치 알아냄
                class_declarations.append((node.name, node.position[0]))

        for class_name, class_position in class_declarations:
            string_literals = extract_string_literals(tree) # 클래스에 존재하는 문자열들 추출
            if not string_literals:
                continue

            updated_source_code = run(source_code, decryptor_class_path, key_cecryptor_class_path, class_name, class_position, string_literals)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_source_code)


def run(source_code, decryptor_class_path, key_cecryptor_class_path, class_name, class_position, string_literals):  
    encrypt_str = StringObfuscate(class_name, class_position)

    encrypt_str.split_source_code(source_code)

    encrypt_str.count += 1

    encrypted_literals = encrypt_str.encrypt_string_literals(string_literals) #문자열 암호화
    encrypt_str.replace_string_literals(string_literals) #문자열 호출을 복호화된 배열참조로 변경
    encrypt_str.insert_encrypted_string_array(encrypted_literals) #소스코드에 배열 삽입

    encrypt_str.encrypt_aes_key() # 키 암호화
    encrypt_str.insert_encryption_key() # 암호화 키 삽입
    
    if encrypt_str.count == encrypt_str.random:
        encrypt_str.insert_decryptor_class(decryptor_class_path, key_cecryptor_class_path)  # 복호화 클래스 삽입
        encrypt_str.decryptor_class = class_name
    
    return encrypt_str.lines


def main():
    # java_folder_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/test'  
    java_folder_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/test'  

    java_files = parse_java_files(java_folder_path)

    # decryptor_class_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/AES.java' 
    # key_decryptor_class_path = "C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/keyDecryptJava.java"

    decryptor_class_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/AES.java' 
    key_decryptor_class_path = "C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/keyDecryptJava.java"

    execute(java_files,decryptor_class_path,key_decryptor_class_path) 
    

if __name__ == "__main__":
    main()
