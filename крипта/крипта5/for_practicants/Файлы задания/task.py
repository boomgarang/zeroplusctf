import base64

dec = input('please, enter string to encrypt: ')
key = '0mN0mP0W3R'
enc = ''

for i in range(len(dec)):
    enc += chr(ord(dec[i]) ^ ord(key[i % len(key)]))

print(base64.b64encode(bytes(enc, 'utf-8')))

