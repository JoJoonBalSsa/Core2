import aes
import keyObfuscate

key = 0x123456789ABCDEF0
seed = 12345 #key의 앞 5자리 예정
plaintext = b'This is a test message. It is longer than 16 bytes.'
filename = "key.txt"
build_def(key,seed,filename)
en_key, encrypted = str_en(filename,seed,plaintext)
str_de(en_key, encrypted)