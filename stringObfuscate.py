from aes import AES
from keyObfuscate import KeyObfuscate
import os

class stringObfuscate:
    aes_key = 0
    key_key = 0

    
    def __init__(self):
        self.encryption_key = os.urandom(16)
        self.key_key = os.urandom(16)


    def encrypt_string(self, plaintext):
        aes = AES()
        encrypted_string = aes.encrypt_string(plaintext, self.encryption_key)
        return encrypted_string
    

    def decrypt_string(self, encrypted_string, aes_key):
        aes = AES()
        decrypted_string = aes.decrypt_string(encrypted_string, aes_key)
        return decrypted_string
    

    def encrypt_key(self):
        keyObfuscate = KeyObfuscate()
        obfuscated_key = keyObfuscate.key_encrypt(self.encryption_key, self.key_key)
        return obfuscated_key
    

    def decrypt_key(self, obfuscated_key, key_key):
        keyObfuscate = KeyObfuscate()
        aes_key = keyObfuscate.key_decrypt(obfuscated_key, key_key)
        return aes_key  