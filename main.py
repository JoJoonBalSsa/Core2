from aes import AES

def test_aes_encryption():
    # AES 인스턴스 생성
    aes = AES()

    # 테스트할 평문과 암호화 키 설정
    plaintext = "Hello, World! This is a test message."
    encryption_key = "MySecretEncryptionKey"

    print("원본 평문:", plaintext)
    print("암호화 키:", encryption_key)

    # 평문을 바이트로 변환
    plaintext_bytes = plaintext.encode('utf-8')

    # 암호화
    encrypted_string = aes.encrypt_string(plaintext_bytes, encryption_key)
    print("암호화된 문자열:", encrypted_string)

    # 복호화
    decrypted_bytes = aes.decrypt_string(encrypted_string, encryption_key)
    decrypted_string = decrypted_bytes.decode('utf-8')

    print("복호화된 평문:", decrypted_string)

    # 원본 평문과 복호화된 평문 비교
    assert plaintext == decrypted_string, "원본 평문과 복호화된 평문이 일치하지 않습니다."
    print("테스트 성공: 원본 평문과 복호화된 평문이 일치합니다.")

if __name__ == "__main__":
    test_aes_encryption()