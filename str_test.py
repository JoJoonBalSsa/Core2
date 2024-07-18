import os
import hashlib
from functools import reduce
import random
R1 = random.getrandbits(64)
R2 = random.getrandbits(64)
R3 = random.getrandbits(64)

def left_shift(data, shift_by):
    return (data << shift_by) & 0xFFFFFFFFFFFFFFFF | (data >> (64 - shift_by))

def right_shift(data, shift_by):
    return (data >> shift_by) | (data << (64 - shift_by)) & 0xFFFFFFFFFFFFFFFF

def bit_inversion(data):
    return data ^ 0xFFFFFFFFFFFFFFFF

def hash_function(data):
    hash_object = hashlib.sha256()
    hash_object.update(data.to_bytes(8, byteorder='big'))
    return int.from_bytes(hash_object.digest()[:8], byteorder='big')

def transform_4bit_segments(hex_number):
    hex_string = f"{hex_number:016X}"
    segments = [hex_string[i:i+1] for i in range(len(hex_string))]
    new_segments = []
    for i in range(0, len(segments), 4):
        block = segments[i:i+4]
        reordered_block = [block[2], block[3], block[0], block[1]]
        new_segments.extend(reordered_block)
    reordered_hex_string = ''.join(new_segments)
    
    return int(reordered_hex_string, 16)

def inverse_transform_4bit_segments(hex_number):
    hex_string = f"{hex_number:016X}"
    segments = [hex_string[i:i+1] for i in range(len(hex_string))]
    new_segments = []
    for i in range(0, len(segments), 4):
        block = segments[i:i+4]
        inverse_block = [block[2], block[3], block[0], block[1]]
        new_segments.extend(inverse_block)
    reordered_hex_string = ''.join(new_segments)
    return int(reordered_hex_string, 16)

def transform_number(data):
    hex_string = f"{data:016X}"
    parts = [hex_string[i:i+4] for i in range(0, len(hex_string), 4)]
    reordered_parts = [parts[2], parts[0], parts[3], parts[1]]
    reordered_hex_string = ''.join(reordered_parts)
    return int(reordered_hex_string, 16)

def inverse_transform_number(data):
    hex_string = f"{data:016X}"
    parts = [hex_string[i:i+4] for i in range(0, len(hex_string), 4)]
    reordered_parts = [parts[1], parts[3], parts[0], parts[2]]
    reordered_hex_string = ''.join(reordered_parts)
    return int(reordered_hex_string, 16)

def key_encrypt(key):
    H1 = hash_function(R1)
    H2 = hash_function(R2)
    H3 = hash_function(R3)
    M1 = key ^ R1
    S1 = left_shift(M1, 5)  # 5비트 왼쪽으로 shift
    X1 = S1 ^ H1
    S2 = right_shift(X1, 3)  # 3비트 오른쪽으로 shift
    M2 = S2 ^ R2
    B2 = bit_inversion(M2)
    X2 = B2 ^ H2
    E = (X2 ^ R3) + H3  # 최종 암호화된 키 생성
    return E

def key_decrypt(encrypted_key):
    H1 = hash_function(R1)
    H2 = hash_function(R2)
    H3 = hash_function(R3)
    X2 = (encrypted_key - H3) ^ R3
    B2 = X2 ^ H2
    M2 = bit_inversion(B2)
    S2 = M2 ^ R2
    B1 = left_shift(S2, 3)  # 3비트 왼쪽으로 shift
    S1 = B1 ^ H1
    M1 = right_shift(S1, 5)  # 5비트 오른쪽으로 shift
    key = M1 ^ R1
    return key

def key2_encrypt(key):
    R4 = random.getrandbits(64)
    R5 = random.getrandbits(64)
    R6 = random.getrandbits(64)
    H1 = hash_function(R4)
    H2 = hash_function(R5)
    H3 = hash_function(R6)
    key = key ^ R1
    key = left_shift(key,5)
    key = key ^ H1
    key = right_shift(key,3)
    key = key ^ R2
    key = bit_inversion(key)
    key = key ^ H2
    key = transform_number(key)
    key = key ^ R3
    key = transform_4bit_segments(key)
    E = key ^ H3
    return E, R4, R5, R6

def key2_decrypt(E, R4, R5, R6):
    H4 = hash_function(R4)
    H5 = hash_function(R5)
    H6 = hash_function(R6)
    key = E ^ H4
    key = inverse_transform_4bit_segments(key)
    key = key ^ R4
    key = inverse_transform_number(key)
    key = key ^ H5
    key = bit_inversion(key)
    key = key ^ R5
    key = left_shift(key, 3)
    key = key ^ H6
    key = right_shift(key, 5)
    key = key ^ R6
    return key

def key_schedule(key, rounds):
    schedule = [key]
    for i in range(1, rounds):
        new_key = hashlib.sha256(schedule[-1]).digest()
        schedule.append(new_key)
    return schedule

def feistel_network(block, round_key):
    left, right = block[:8], block[8:]
    f_result = bytes(a ^ b for a, b in zip(right, round_key[:8]))
    new_right = bytes(a ^ b for a, b in zip(left, f_result))
    return right + new_right

def inverse_feistel_network(block, round_key):
    left, right = block[:8], block[8:]
    f_result = bytes(a ^ b for a, b in zip(left, round_key[:8]))
    new_left = bytes(a ^ b for a, b in zip(right, f_result))
    return new_left + left

def str_encrypt(data, key, rounds=16):
    key_sched = key_schedule(key, rounds)
    encrypted = bytearray()
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        if len(block) < 16:
            block = block.ljust(16, b'\x00')
        for round_key in key_sched:
            block = feistel_network(block, round_key)
        encrypted.extend(block)
    return bytes(encrypted)

def str_decrypt(data, key, rounds=16):
    key_sched = key_schedule(key, rounds)
    decrypted = bytearray()
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        for round_key in reversed(key_sched):
            block = inverse_feistel_network(block, round_key)
        decrypted.extend(block)
    return bytes(decrypted).rstrip(b'\x00')

def save_key_to_file(encrypted_key, filename):
    with open(filename, 'w') as file:
        encrypted_key = str(encrypted_key)
        file.write(encrypted_key)

def load_key_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
def build_def(key, filename):
    encrypted_key = key_encrypt(key)
    print(f"Encrypted key: {encrypted_key:016X}")
    save_key_to_file(encrypted_key, filename)

def str_en(filename,plaintext):
    key = load_key_from_file(filename)
    key = int(key)
    decrypted_key = key_decrypt(key)
    print(f"Decrypted key: {decrypted_key:016X}")
    en_key,R4,R5,R6 = key2_encrypt(decrypted_key)
    en_key = en_key.to_bytes(8, byteorder='big')
    encrypted = str_encrypt(plaintext, en_key)
    print("Encrypted:", encrypted)
    return en_key, encrypted

def str_de(en_key, encrypted):
    decrypted = str_decrypt(encrypted, en_key)
    print("Decrypted (as text):", decrypted.decode('utf-8'))

# 테스트
key = os.urandom(16)
key = int.from_bytes(key, byteorder='big')
plaintext = b'This is a test message. It is longer than 16 bytes.'
filename = "key.txt"
build_def(key,filename)
en_key, encrypted = str_en(filename,plaintext)
str_de(en_key, encrypted)