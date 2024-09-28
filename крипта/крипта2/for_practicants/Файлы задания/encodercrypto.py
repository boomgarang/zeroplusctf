flag = ""
encoded_flag = ""

for char in flag:
    encoded_flag += str(ord(char)) + " "

print(encoded_flag.strip())
