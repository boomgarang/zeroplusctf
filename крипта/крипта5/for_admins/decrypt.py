import base64

enc = input('please, enter string to decrypt: ')
key = '0mN0mP0W3R'
dec = ''

enc = base64.b64decode(enc).decode('utf-8')

for i in range(len(enc)):
    dec += chr(ord(enc[i]) ^ ord(key[i % len(key)]))

print(dec)

