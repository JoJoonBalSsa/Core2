from aes import AES
from keyObfuscate import KeyObfuscate
import os

def test_aes_encryption():
    # AES 인스턴스 생성
    aes = AES()

    # 테스트할 평문과 암호화 키 설정
    plaintext = "Hello, World! This is a test message."
    encryption_key = os.urandom(16)
    key_key = os.urandom(16)

    print("원본 평문:", plaintext)
    print("암호화 키:", encryption_key)
    print("키 암호화 키:", key_key.hex())


    # 암호화
    encrypted_string = aes.encrypt_string(plaintext, encryption_key)
    print("암호화된 문자열:", encrypted_string)


    # 키 암호화
    keyObfuscate = KeyObfuscate()
    obfuscated_key = keyObfuscate.key_encrypt(encryption_key, key_key)  
    print("암호화된 키:", obfuscated_key.hex())


    # 키 복호화
    decrypted_key = keyObfuscate.key_decrypt(obfuscated_key, key_key).hex()
    print("복호화된 키:", decrypted_key)
    

    # 복호화
    decrypted_string = aes.decrypt_string(encrypted_string, decrypted_key)
    print("복호화된 평문:", decrypted_string)


if __name__ == "__main__":
    test_aes_encryption()