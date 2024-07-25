import hashlib

class KeyObfuscate:

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
    
    
    def key_encrypt(self, aes_key, key2):
        enc2_aes_key = self.alg2_encrypt(aes_key, key2)
                                      
        return enc2_aes_key  
    

    def key_decrypt(self, enc2_aes_key, key2):

        enc_aes_key = self.alg2_decrypt(enc2_aes_key, key2)
        return enc_aes_key