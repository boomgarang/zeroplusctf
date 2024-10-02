#include <iostream>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <thread>
#include <string>

using namespace std;
using namespace std::chrono;

// Функция для получения случайного числа в диапазоне
int getRandomNumber(int min, int max) {
    return rand() % (max - min + 1) + min;
}

// Основная функция для генерации примеров и проверки ввода
void mathGame() {
    const int TOTAL_ATTEMPTS = 500; // количество примеров
    int correctAnswers = 0;
    string userInput;

    while (correctAnswers < TOTAL_ATTEMPTS) {
        // Генерация случайных чисел и операции
        int num1 = getRandomNumber(1, 100);
        int num2 = getRandomNumber(1, 100);
        char operation = getRandomNumber(0, 2) == 0 ? '+' : '*'; // + или *
        int correctResult = (operation == '+') ? (num1 + num2) : (num1 * num2);

        // Вывод примера
        cout << "Solve: " << num1 << " " << operation << " " << num2 << " = ?" << endl;
        cout.flush(); // Явно сбрасываем вывод, чтобы он немедленно отправился клиенту

        // Замер времени для ожидания ввода
        auto start = high_resolution_clock::now();

        getline(cin, userInput); // Чтение ответа в виде строки
        auto end = high_resolution_clock::now();
        duration<double> elapsed = end - start;

        // Проверка на время
        if (elapsed.count() > 2.0) {
            cout << "Slow! You took too long." << endl;
            cout.flush();
            correctAnswers = 0; // Сброс прогресса
            continue;
        }

        // Преобразование ответа пользователя в число
        int userAnswer;
        try {
            userAnswer = stoi(userInput); // Попытка преобразования строки в число
        } catch (...) {
            cout << "Invalid input! Please enter a valid number." << endl;
            cout.flush();
            correctAnswers = 0; // Сброс прогресса
            continue;
        }

        // Проверка ответа
        if (userAnswer == correctResult) {
            correctAnswers++;
            cout << "Correct! " << correctAnswers << "/" << TOTAL_ATTEMPTS << endl;
            cout.flush();
        } else {
            cout << "Wrong! Starting over..." << endl;
            cout.flush();
            correctAnswers = 0; // Сброс прогресса
        }
    }

    // Если игрок ответил правильно на 500 примеров
    cout << "KpkCTF{1ou_c0unT_V3ry_We11}" << endl;
    cout.flush();
}

int main() {
    srand(static_cast<unsigned int>(time(0))); // Инициализация генератора случайных чисел
    mathGame(); // Запуск игры
    return 0;
}
