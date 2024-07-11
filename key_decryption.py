from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
'''
런타임 때 실행
'''
#키 파일 불러오기
def load_key_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()
#복호화 진행
def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

def decrypt_key(encrypted_key, encryption_key):
    encryption_key = encryption_key.ljust(32)[:32].encode('utf-8')  # 키를 32바이트로 패딩 또는 잘라내기
    encrypted_key = binascii.unhexlify(encrypted_key)
    iv = encrypted_key[:16]  # 처음 16바이트는 IV
    encrypted_key = encrypted_key[16:]  # 나머지는 실제 암호화된 키
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    padded_key = cipher.decrypt(encrypted_key)
    key = unpad(padded_key)
    return key

#test
filename = "key.txt"
second_key = "anothersecurekey1234567890"
key = load_key_from_file(filename)
decrypted_key = decrypt_key(key, second_key)
print("Decrypted Key:", binascii.hexlify(decrypted_key).decode('utf-8'))