import aes
import keyObfuscate
import os
import binascii

AES = aes.AES()


# 테스트
key = os.urandom(16)  # 16바이트 키
plaintext = "anothersecurekey1234567890"

print("Key:", binascii.hexlify(key).decode('utf-8'))
encrypted_key = encrypt_key(key, plaintext)
print("Encrypted Key:", encrypted_key)

decrypted_key = decrypt_key(encrypted_key, plaintext)
print("Decrypted Key:", binascii.hexlify(decrypted_key).decode('utf-8'))





key = 0x123456789ABCDEF0
seed = 12345 #key의 앞 5자리 예정
plaintext = b'This is a test message. It is longer than 16 bytes.'
filename = "key.txt"
AES.build_def(key,seed,filename)
en_key, encrypted = AES.str_en(filename,seed,plaintext)
AES.str_de(en_key, encrypted)