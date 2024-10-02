print("Физик немного поколдовал, и все сломалось. Почини, пожалуйста, и получишь магию")
def caesar_cipher_decoder(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result
def block_permutation_decipher(shifted_text, block_size):
    result = ""
    for i in range(0, len(shifted_text), block_size):
        result += shifted_text[i:i+block_size][::-1]
    return result


shifted_text = "ywhbOD{1ydq1gmv30r_gh0b_gg1l3_}h"
shift = int(input("Введите количество слов из истории: "))
block_size = 5
decoded_text = caesar_cipher_decoder(shifted_text, -shift)
decipher_text = block_permutation_decipher(shifted_text, -block_size)
decoded_texts = caesar_cipher_decoder(decipher_text, -shift)
print(decoded_texts)