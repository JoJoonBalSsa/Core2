import hashlib
import random

class KeyObfuscate:
    # __R1 = 0
    # __R2 = 0
    # __R3 = 0
    # __R4 = 0
    # __R5 = 0
    # __R6 = 0


    # def alg1_init_rval(self):                  
    #     self.__R1 = random.getrandbits(64)
    #     self.__R2 = random.getrandbits(64)
    #     self.__R3 = random.getrandbits(64)
    #     self.__R4 = random.getrandbits(64)
    #     self.__R5 = random.getrandbits(64)
    #     self.__R6 = random.getrandbits(64)


    # def alg1_left_shift(self, data, shift_by):
    #     return (data << shift_by) & 0xFFFFFFFFFFFFFFFF | (data >> (64 - shift_by))
    

    # def alg1_right_shift(self, data, shift_by):
    #     return (data >> shift_by) | (data << (64 - shift_by)) & 0xFFFFFFFFFFFFFFFF
    

    # def alg1_bit_inversion(self, data):
    #     return data ^ 0xFFFFFFFFFFFFFFFF
    

    # def alg1_hashing(self, data):
    #     hash_object = hashlib.sha256()
    #     hash_object.update(data.to_bytes(8, byteorder='big'))
    #     return int.from_bytes(hash_object.digest()[:8], byteorder='big')
    

    # def alg1_transform_4bit_segments(self, hex_number):
    #     hex_string = f"{hex_number:016X}"
    #     segments = [hex_string[i:i+1] for i in range(len(hex_string))]
    #     new_segments = []
    #     for i in range(0, len(segments), 4):
    #         block = segments[i:i+4]
    #         reordered_block = [block[2], block[3], block[0], block[1]]
    #         new_segments.extend(reordered_block)
    #     reordered_hex_string = ''.join(new_segments)
        
    #     return int(reordered_hex_string, 16)
    

    # def alg1_inverse_transform_4bit_segments(self, hex_number):
    #     hex_string = f"{hex_number:016X}"
    #     segments = [hex_string[i:i+1] for i in range(len(hex_string))]
    #     new_segments = []
    #     for i in range(0, len(segments), 4):
    #         block = segments[i:i+4]
    #         inverse_block = [block[2], block[3], block[0], block[1]]
    #         new_segments.extend(inverse_block)
    #     reordered_hex_string = ''.join(new_segments)
    #     return int(reordered_hex_string, 16)
    

    # def alg1_transform_number(self, data):
    #     hex_string = f"{data:016X}"
    #     parts = [hex_string[i:i+4] for i in range(0, len(hex_string), 4)]
    #     reordered_parts = [parts[2], parts[0], parts[3], parts[1]]
    #     reordered_hex_string = ''.join(reordered_parts)
    #     return int(reordered_hex_string, 16)
    

    # def alg1_inverse_transform_number(self, data):
    #     hex_string = f"{data:016X}"
    #     parts = [hex_string[i:i+4] for i in range(0, len(hex_string), 4)]
    #     reordered_parts = [parts[1], parts[3], parts[0], parts[2]]
    #     reordered_hex_string = ''.join(reordered_parts)
    #     return int(reordered_hex_string, 16)
    

    # def alg1_encrypt(self, key):         
    #     self.alg1_init_rval()

    #     H1 = self.alg1_hashing(self.__R1)
    #     H2 = self.alg1_hashing(self.__R2)
    #     H3 = self.alg1_hashing(self.__R3)
    #     M1 = key ^ self.__R1
    #     S1 = self.alg1_left_shift(M1, 5)  # 5비트 왼쪽으로 shift
    #     X1 = S1 ^ H1
    #     S2 = self.alg1_right_shift(X1, 3)  # 3비트 오른쪽으로 shift
    #     M2 = S2 ^ self.__R2
    #     B2 = self.alg1_bit_inversion(M2)
    #     X2 = B2 ^ H2
    #     E = (X2 ^ self.__R3) + H3  # 최종 암호화된 키 생성
    #     return E
    

    # def alg1_decrypt(self, encrypted_key):
    #     H1 = self.alg1_hashing(self.__R1)
    #     H2 = self.alg1_hashing(self.__R2)
    #     H3 = self.alg1_hashing(self.__R3)
    #     X2 = (encrypted_key - H3) ^ self.__R3
    #     B2 = X2 ^ H2
    #     M2 = self.alg1_bit_inversion(B2)
    #     S2 = M2 ^ self.__R2
    #     B1 = self.alg1_left_shift(S2, 3)  # 3비트 왼쪽으로 shift
    #     S1 = B1 ^ H1
    #     M1 = self.alg1_right_shift(S1, 5)  # 5비트 오른쪽으로 shift
    #     key = M1 ^ self.__R1
    #     return key
    

    def alg2_key_schedule(self, key, rounds):
        schedule = [key]
        for i in range(1, rounds):
            new_key = hashlib.sha256(schedule[-1]).digest()
            schedule.append(new_key[:16])  # 16바이트로 제한
        return schedule


    def alg2_feistel_network(self, block, round_key):
        left, right = block[:8], block[8:]
        f_result = bytes(a ^ b for a, b in zip(right, round_key[:8]))
        new_right = bytes(a ^ b for a, b in zip(left, f_result))
        return right + new_right


    def alg2_inverse_feistel_network(self, block, round_key):
        left, right = block[:8], block[8:]
        f_result = bytes(a ^ b for a, b in zip(left, round_key[:8]))
        new_left = bytes(a ^ b for a, b in zip(right, f_result))
        return new_left + left


    def alg2_encrypt(self, data, key, rounds=16):
        key_sched = self.alg2_key_schedule(key, rounds)
        encrypted = bytearray()
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            for round_key in key_sched:
                block = self.alg2_feistel_network(block, round_key)
            encrypted.extend(block)
        return bytes(encrypted)


    def alg2_decrypt(self, data, key, rounds=16):
        key_sched = self.alg2_key_schedule(key, rounds)
        decrypted = bytearray()
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            for round_key in reversed(key_sched):
                block = self.alg2_inverse_feistel_network(block, round_key)
            decrypted.extend(block)
        return bytes(decrypted).rstrip(b'\x00')
    

    # def alg3_encrypt(self, key):
    #     H4 = self.alg1_hashing(self.__R4)
    #     H5 = self.alg1_hashing(self.__R5)
    #     H6 = self.alg1_hashing(self.__R6)
    #     key = key ^ self.__R4
    #     key = self.alg1_left_shift(key,5)
    #     key = key ^ H4
    #     key = self.alg1_right_shift(key,3)
    #     key = key ^ self.__R5
    #     key = self.alg1_bit_inversion(key)
    #     key = key ^ H5
    #     key = self.alg1_transform_number(key)
    #     key = key ^ self.__R6
    #     key = self.alg1_transform_4bit_segments(key)
    #     E = key ^ H6
    #     return E  
    

    # def alg3_decrypt(self, E):
    #     H4 = self.alg1_hashing(self.__R4)
    #     H5 = self.alg1_hashing(self.__R5)
    #     H6 = self.alg1_hashing(self.__R6)
    #     key = E ^ H6
    #     key = self.alg1_inverse_transform_4bit_segments(key)
    #     key = key ^ self.__R6
    #     key = self.alg1_inverse_transform_number(key)
    #     key = key ^ H5
    #     key = self.alg1_bit_inversion(key)
    #     key = key ^ self.__R5
    #     key = self.alg1_left_shift(key, 3)
    #     key = key ^ H4
    #     key = self.alg1_right_shift(key, 5)
    #     key = key ^ self.__R4
    #     return key
    

    def key_encrypt(self, aes_key, key2):

        #enc_aes_key = self.alg1_encrypt(aes_key)

        #enc_aes_key = enc_aes_key.to_bytes(16, 'big') 
        enc2_aes_key = self.alg2_encrypt(aes_key, key2)
                                      
        return enc2_aes_key  
    

    def key_decrypt(self, enc2_aes_key, key2):

        enc_aes_key = self.alg2_decrypt(enc2_aes_key, key2)

        #enc_aes_key = int.from_bytes(enc_aes_key, 'big')
        #aes_key = self.alg1_decrypt(enc_aes_key)

        return enc_aes_key