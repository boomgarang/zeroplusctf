encoded_flag = "65 110 116 105 107 112 107 49 123 115 111 117 108 95 111 102 95 65 114 109 101 110 105 97 125"
decoded_flag = ""

for num in encoded_flag.split():
    decoded_flag += chr(int(num))

print(decoded_flag)