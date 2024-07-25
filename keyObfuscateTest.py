import os
import base64

from keyObfuscate import KeyObfuscate
def int_to_base64(byte_representation):
    base64_bytes = base64.b64encode(byte_representation)
    
    # 바이트를 문자열로 디코딩
    base64_string = base64_bytes.decode('ascii')
    
    return base64_string

def test_key_obfuscate():
    # KeyObfuscate 인스턴스 생성
    ko = KeyObfuscate()

    # 테스트용 키와 데이터 생성
    key = os.urandom(16)
    data = os.urandom(32)

    # 암호화 및 복호화 테스트
    encrypted = ko.alg2_encrypt(data, key)
    decrypted = ko.alg2_decrypt(encrypted, key)
    assert data == decrypted, "암호화 및 복호화 실패"

    # 키 스케줄 테스트
    key_schedule = ko.alg2_key_schedule(key, 16)
    assert len(key_schedule) == 16, "키 스케줄 길이 불일치"
    assert all(len(k) == 16 for k in key_schedule), "키 스케줄의 키 길이 불일치"

    # Feistel 네트워크 테스트
    block = os.urandom(16)
    round_key = os.urandom(16)
    encrypted_block = ko.alg2_feistel_network(block, round_key)
    decrypted_block = ko.alg2_inverse_feistel_network(encrypted_block, round_key)
    assert block == decrypted_block, "Feistel 네트워크 암호화/복호화 실패"

    # 키 암호화/복호화 테스트
    aes_key = os.urandom(16)
    key2 = os.urandom(8)
    encrypted_aes_key = ko.key_encrypt(aes_key, key2)

    print(int_to_base64(key2))
    print(int_to_base64(encrypted_aes_key))
    print(int_to_base64(aes_key))
    decrypted_aes_key = ko.key_decrypt(encrypted_aes_key, key2)
    assert aes_key == decrypted_aes_key, "키 암호화/복호화 실패"

    print("모든 테스트 통과!")

if __name__ == "__main__":
    test_key_obfuscate()