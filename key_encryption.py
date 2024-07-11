from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
'''
빌드 때 실행
'''

#암호화
def pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt_key(key, encryption_key):
    encryption_key = encryption_key.ljust(32)[:32].encode('utf-8')  # 키를 32바이트로 패딩 또는 잘라내기
    iv = get_random_bytes(16)  # 16바이트 IV 생성
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    padded_key = pad(key, AES.block_size)
    encrypted_key = iv + cipher.encrypt(padded_key)
    return binascii.hexlify(encrypted_key).decode('utf-8')

#키 파일 생성
def save_key_to_file(encrypted_key, filename):
    with open(filename, 'w') as file:
        file.write(encrypted_key)

#test        
key = get_random_bytes(32)
print(key)
second_key = "anothersecurekey1234567890"
encrypted_key = encrypt_key(key, second_key)
print("Encrypted Key:", encrypted_key)

filename = "key.txt"
save_key_to_file(encrypted_key, filename)