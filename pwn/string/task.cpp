#include <stdio.h>



void win() {
    FILE *file;
    char buffer[256]; // Буфер для чтения данных

    // Открытие файла FLAG.MD для чтения
    file = fopen("FLAG.MD", "r");
    if (file == NULL) {
        printf("Ошибка: не удалось открыть файл FLAG.MD\n");
        return;
    }

    // Чтение строки из файла и вывод её на экран
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }

    // Закрытие файла
    fclose(file);
}


void read_function() {
    char buffer[64];
    int flag1 = 0;
    int flag2 = 44;

    printf("Enter your input: ");
    scanf("%s", buffer);  // Небезопасно: нет ограничения длины ввода

    printf("You flag1: %d\n", flag1);

    printf("You flag2: %d\n", flag2);
    if (flag1 == 64 && flag2 == 21) {
        win();
    } else {
        printf("You entered: %s\n", buffer);
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    read_function();
    return 0;
}
