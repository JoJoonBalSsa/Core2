from aes import AES
import os

def test_aes_encryption():
    # AES 인스턴스 생성
    aes = AES()

    # 테스트할 평문과 키 생성
    plaintext = b"Hello, World! This is a test message."
    key = os.urandom(16)  # 128비트(16바이트) 키 생성

    # 암호화 키 (사용자 지정 문자열)
    encryption_key = "MySecretEncryptionKey"

    print("원본 평문:", plaintext)
    print("원본 키:", key.hex())

    # 키 암호화
    encrypted_key = aes.encrypt_key(key, encryption_key)
    print("암호화된 키:", encrypted_key)

    # 키 복호화
    decrypted_key = aes.decrypt_key(encrypted_key, encryption_key)
    print("복호화된 키:", decrypted_key.hex())

    # 평문을 16바이트 블록으로 패딩
    padded_plaintext = aes.pad(plaintext, 16)

    # 암호화
    ciphertext = b""
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        encrypted_block = aes.aes_encrypt_block(block, key)
        ciphertext += encrypted_block

    print("암호문:", ciphertext.hex())

    # 복호화
    decrypted_text = b""
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = aes.aes_decrypt_block(block, key)
        decrypted_text += decrypted_block

    # 패딩 제거
    unpadded_text = aes.unpad(decrypted_text)

    print("복호화된 평문:", unpadded_text.decode('utf-8'))

    # 원본 평문과 복호화된 평문 비교
    assert plaintext == unpadded_text, "원본 평문과 복호화된 평문이 일치하지 않습니다."
    print("테스트 성공: 원본 평문과 복호화된 평문이 일치합니다.")

if __name__ == "__main__":
    test_aes_encryption()