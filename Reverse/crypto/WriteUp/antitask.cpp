#include <iostream>
#include <fstream>
#include <string>

// Функция для XOR-шифрования (обратима, та же используется для шифрования и дешифрования)
std::string xorEncrypt(const std::string& input, char key) {
    std::string output = input;
    for (size_t i = 0; i < input.size(); ++i) {
        output[i] = input[i] ^ key; // XOR с ключом
    }
    return output;
}

// Функция для обратного шифра Цезаря (сдвиг на отрицательное количество позиций)
std::string caesarShiftDecrypt(const std::string& input, int shift) {
    std::string output = input;
    for (size_t i = 0; i < input.size(); ++i) {
        char shifted = input[i];
        if (isalpha(shifted)) {
            char base = islower(shifted) ? 'a' : 'A';
            shifted = (shifted - base + (26 - shift)) % 26 + base; // Обратный шифр Цезаря
        }
        output[i] = shifted;
    }
    return output;
}

// Функция для обратного циклического сдвига битов
std::string bitwiseRotateDecrypt(const std::string& input, int rotateBy) {
    std::string output = input;
    for (size_t i = 0; i < input.size(); ++i) {
        unsigned char ch = input[i];
        ch = (ch >> rotateBy) | (ch << (8 - rotateBy)); // Обратный циклический сдвиг
        output[i] = ch;
    }
    return output;
}

// Основная функция дешифрования строки
std::string decrypt(const std::string& input) {
    std::string step1 = bitwiseRotateDecrypt(input, 3);  // Шаг 1: Обратный циклический сдвиг на 3 бита вправо
    std::string step2 = caesarShiftDecrypt(step1, 5);    // Шаг 2: Обратный шифр Цезаря с сдвигом на 5
    std::string step3 = xorEncrypt(step2, 0xAA);         // Шаг 3: XOR с тем же ключом 0xAA
    return step3;
}

// Функция для чтения строки из файла
std::string readFromFile(const std::string& filename) {
    std::ifstream infile(filename);
    if (!infile) {
        std::cerr << "Не удалось открыть файл: " << filename << std::endl;
        exit(1);
    }
    std::string content((std::istreambuf_iterator<char>(infile)),
                         std::istreambuf_iterator<char>());
    return content;
}

// Функция для записи строки в файл
void writeToFile(const std::string& filename, const std::string& content) {
    std::ofstream outfile(filename);
    if (!outfile) {
        std::cerr << "Не удалось открыть файл для записи: " << filename << std::endl;
        exit(1);
    }
    outfile << content;
}

int main() {
    std::string inputFilename = "encrypted.txt";  // Файл с зашифрованной строкой
    std::string outputFilename = "2_decrypted.txt"; // Файл для записи расшифрованной строки

    // Чтение зашифрованной строки из файла
    std::string encrypted = readFromFile(inputFilename);
    std::cout << "Прочитанная зашифрованная строка: " << encrypted << std::endl;

    // Дешифрование строки
    std::string decrypted = decrypt(encrypted);
    std::cout << "Расшифрованная строка: " << decrypted << std::endl;

    // Запись расшифрованной строки в файл
    writeToFile(outputFilename, decrypted);
    std::cout << "Расшифрованная строка записана в файл: " << outputFilename << std::endl;

    return 0;
}
