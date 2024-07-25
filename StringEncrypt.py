import javalang
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
#from aes import AES

class Encrypt_str:
    def __init__(self, aes_key=None):
        self.aes_key = base64.b64encode(os.urandom(16)).decode('utf-8')
        self.enc_aes_key = os.urandom(16).hex()
        self.enc_enc_aes_key = os.urandom(16).hex()
        self.count = 0 # 복호화 코드 삽입할 소스코드
        self.random = 1 # 랜덤으로 소스코드 정하기
        self.decryptor_package = None
        self.decryptor_class = None
    
    def parse_java_files(self, folder_path): # 소스코드 => AST tree
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

    def extract_string_literals(self, tree): # AST 에서 문자열 찾아내고 문자열 값과 위치 저장
        string_literals = []
        for path, node in tree:
            if isinstance(node, javalang.tree.Literal) and isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
                string_literals.append((node.value, node.position))
        return string_literals
    
    def encrypt(self, plain_text, key):
        key_bytes = base64.b64decode(key)  # Convert key to bytes
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_text = pad(plain_text.encode('utf-8'), AES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted_text).decode('utf-8')
    
    def encrypt_string_literals(self, string_literals): # 암호화
        encrypted_literals = [self.encrypt(literal, self.aes_key) for literal, _ in string_literals]
        
        return encrypted_literals

    def replace_string_literals(self, source_code, string_literals, class_name):
        lines = source_code.split('\n')
        string_literals_sorted = sorted(string_literals, key=lambda x: (x[1][0], -x[1][1]))  # 라인 오른쪽부터 문자열 변환
        for index, (literal, position) in enumerate(string_literals_sorted):
            line_index = position[0] - 1
            column_index = position[1] - 1
            line = lines[line_index]
            end_column_index = column_index + len(literal)
            new_line = line[:column_index] + f'STRING_LITERALS_{class_name.upper()}[{index}]' + line[end_column_index:]
            lines[line_index] = new_line
        return '\n'.join(lines)

    def  insert_encrypted_string_array(self,source_code, encrypted_literals, class_name, class_position): # 문자열이 원래 있던 자리를 배열참조로 바꿈
        # 지금은 STRING_LITERALS_{class 이름} 인데 바꿔도됨
        array_declaration = f'public static final String[] STRING_LITERALS_{class_name.upper()} = {{\n' + ',\n'.join(f'"{literal}"' for literal in encrypted_literals) + '\n};\n'
        lines = source_code.split('\n')
        lines.insert(class_position, array_declaration)
        reflection = 'import java.lang.reflect.Method;'
        if reflection not in lines:
                lines.insert(1, reflection)

        # 복호화 코드 삽입
        # decryption_code = f"""
        # static {{
        #     for (int i = 0; i < STRING_LITERALS_{class_name.upper()}.length; i++) {{
        #         STRING_LITERALS_{class_name.upper()}[i] = new String(AES.decrypt(STRING_LITERALS_{class_name.upper()}[i], ENCRYPTION_KEY_{class_name.upper()}.getBytes()));
        #     }}
        # }}
        # """

        decryption_code = f"""
        static{{
		try {{
			Class<?> decryptorClass = Class.forName("christmas.AES");
        Method decryptMethod = decryptorClass.getMethod("decrypt", String.class, String.class);
        for (int i = 0; i < STRING_LITERALS_{class_name.upper()}.length; i++) {{
        STRING_LITERALS_{class_name.upper()}[i] = (String) decryptMethod.invoke(null, STRING_LITERALS_{class_name.upper()}[i], ENCRYPTION_KEY_{class_name.upper()}); 
        }}
		}} catch (Exception e) {{
		}}
		
        }}
        """
        lines.insert(class_position + 2, decryption_code)
        return '\n'.join(lines)
    
    def insert_encryption_key(self, source_code, class_name, class_position, encryption_key): # 키를 난독화하여 문자열에 추가하는 함수
        key_declaration = f'private static final String ENCRYPTION_KEY_{class_name.upper()} = "{encryption_key}";\n'
        lines = source_code.split('\n')
        lines.insert(class_position+1, key_declaration)
        return '\n'.join(lines)


    def encrypt_aes_key(self, aes_key):
        encrypted_aes_key = self.aes.encrypt_string(aes_key.encode('utf-8'), self.enc_aes_key)
        encrypted_enc_aes_key = self.aes.encrypt_string(encrypted_aes_key.encode('utf-8'), self.enc_enc_aes_key)
        return encrypted_enc_aes_key
    
    # def insert_decryptor_class(self, source_code, decryptor_class_path):
    #     with open(decryptor_class_path, 'r', encoding='utf-8') as file:
    #         decryptor_code = file.read()

        
    #     lines = source_code.split('\n')
    #     lines.append(decryptor_code)
    #     return '\n'.join(lines)
    
    def insert_decryptor_class(self,source_code, decryptor_class_path):
        with open(decryptor_class_path, 'r', encoding='utf-8') as file:
            decryptor_code = file.read()

        lines = source_code.split('\n')

        decryptor_code = decryptor_code.split('\n')
        decryptor_code = [line for line in decryptor_code if not line.startswith('import')]
        decryptor_code = '\n'.join(decryptor_code)


        # Import 문 추가
        import_statements = [
            'import javax.crypto.Cipher;',
'import javax.crypto.KeyGenerator;',
'import javax.crypto.SecretKey;',
'import javax.crypto.spec.SecretKeySpec;',
'import java.util.Base64;',
'import java.lang.reflect.Method;'
        ]
        for import_statement in import_statements:
            if import_statement not in lines:
                lines.insert(1, import_statement)

        # AESDecryptor 클래스 추가
        lines.append(decryptor_code)

        return '\n'.join(lines)

    def get_package_name(self, tree): #패키지 이름 알아내기(for reflection)
        for path, node in tree:
            if isinstance(node, javalang.tree.PackageDeclaration):
                return node.name
        return None
    
    def process_java_files(self, java_files,decryptor_class_path):
        for file_path, tree, source_code in java_files:
            class_declarations = []
            self.decryptor_package = self.get_package_name(tree)
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration): #클래스 별로 문자열을 추출할것이기 때문에 클래스 정의 위치 알아냄
                    class_declarations.append((node.name, node.position[0]))

            for class_name, class_position in class_declarations:
                string_literals = self.extract_string_literals(tree) # 클래스에 존재하는 문자열들 추출
                if not string_literals:
                    continue

                self.count += 1

                encrypted_literals = self.encrypt_string_literals(string_literals) #문자열들 암호화

                updated_source_code = self.replace_string_literals(source_code, string_literals, class_name) #문자열 -> 배열참조

                updated_source_code = self.insert_encrypted_string_array(updated_source_code, encrypted_literals, class_name, class_position) #소스코드에 배열 삽입

                #encrypted_key = self.encrypt_aes_key(self.aes_key) # 키를 두번 암호화 # 일단 테스트로 암호화 없이

                updated_source_code = self.insert_encryption_key(updated_source_code, class_name, class_position, self.aes_key) # 암호화 키 삽입
                
                if self.count == self.random:
                    updated_source_code = self.insert_decryptor_class(updated_source_code, decryptor_class_path)  # 복호화 클래스 삽입
                    self.decryptor_class = class_name

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_source_code)


def main():
    java_folder_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/Core2/test'  

    encryptor = Encrypt_str()
    java_files = encryptor.parse_java_files(java_folder_path) 
    decryptor_class_path = 'C:/Users/조준형/Desktop/S개발자_프로젝트/AES.java' 

    encryptor.process_java_files(java_files,decryptor_class_path) 

if __name__ == "__main__":
    main()
