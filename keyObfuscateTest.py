from keyObfuscate import KeyObfuscate
import os


# asdf = KeyObfuscate(aes_key, key2)
def remove_trailing_null_bytes(byte_array):
    # 바이트 배열의 끝에서부터 시작하여 널 바이트가 아닌 첫 번째 바이트를 찾습니다
    i = len(byte_array) - 1
    while i >= 0 and byte_array[i] == 0:
        i -= 1
    
    # 널 바이트가 아닌 마지막 바이트까지의 배열을 반환합니다
    return byte_array[:i+1]


for i in range (0, 10000000):
    aes_key = os.urandom(8)
    key2 = os.urandom(16)


    #aes_key = int.from_bytes(aes_key, 'big')
    asdf = KeyObfuscate(aes_key, key2)

    asdf_key = asdf.key_decrypt(asdf.obfuscated_key, key2)
    aes_key = remove_trailing_null_bytes(aes_key)
    

    print(i)
    
    if aes_key != asdf_key:
        print("original key: " + str(aes_key))
        print("decrypt* key: " + str(asdf_key))
        print("Failed")
        break

        

# aes_key = 0x123456789ABCDEF0
# key2 = 0x123456789ABCDEF0

# asdf_key = asdf.alg1_encrypt(aes_key)
# print(f"alg2_enc: {asdf_key:016X}")

# enc_aes_key = asdf_key.to_bytes(16, 'big') 
# key2_bytes = key2.to_bytes(16, byteorder='big')
# enc2_aes_key = asdf.alg2_encrypt(enc_aes_key, key2_bytes)
# k = int.from_bytes(enc2_aes_key, 'big')
# print(f"alg3_enc: {k:016X}")
                                                                                    
# enc_aes_key = asdf.alg2_decrypt(enc2_aes_key, key2_bytes)
# enc_aes_key = int.from_bytes(enc_aes_key, 'big')
# print(f"alg3_dec: {enc_aes_key:016X}")

# asdf_key = asdf.alg1_decrypt(enc_aes_key)
# print(f"alg2_dec: {asdf_key:016X}")