from keyObfuscate import KeyObfuscate

aes_key = 0x123456789ABCDEF0
key2 = 0x123456789ABCDEF0

asdf = KeyObfuscate(aes_key, key2)

enc_aes_key = asdf.key_encrypt(aes_key)
print(f"alg1_enc: {enc_aes_key:016X}")

enc_aes_key = enc_aes_key.to_bytes(16, 'big') 
key2_bytes = key2.to_bytes(16, byteorder='big')
enc2_aes_key = asdf.str_encrypt(enc_aes_key, key2_bytes)
k = int.from_bytes(enc2_aes_key, 'big')
print(f"alg3_enc: {k:016X}")
                                                                                    
enc_aes_key = asdf.str_decrypt(enc2_aes_key, key2_bytes)
enc_aes_key = int.from_bytes(enc_aes_key, 'big')
print(f"alg3_dec: {enc_aes_key:016X}")

aes_key = asdf.key_decrypt(enc_aes_key)
print(f"alg1_dec: {aes_key:016X}")