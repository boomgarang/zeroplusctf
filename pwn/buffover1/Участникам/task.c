#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char local_storage[64];

void win() {
    FILE *file;
    char buffer[256]; // Буфер для чтения данных

    // Открытие файла FLAG.MD для чтения
    file = fopen("FLAG.MD", "r");
    if (file == NULL) {
        printf("Ошибка: не удалось открыть файл FLAG.MD\n");
        return;
    }

    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }

    // Закрытие файла
    fclose(file);
}




void transform_data(char *data) {
    for (int i = 0; i < strlen(data); i++) {
        if (data[i] >= 'a' && data[i] <= 'z') {
            data[i] -= 32; 
        }
    }
}

int validate_data(char *data) {
    int valid = 1;
    for (int i = 0; i < strlen(data); i++) {
        if (data[i] == ' ' || data[i] == '\n') {
            valid = 0; 
        }
    }
    return valid;
}

void read_data()
{
    char temp_data[64];

    gets(temp_data);

    strcpy(local_storage, temp_data);
}

void process_user_data() {
 
    transform_data(local_storage);

    printf("Processed data: %s\n", local_storage);
}



int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char initial_message[] = "Initializing data processing...\n";
    char processed_message[100];
   


    // Ненужное копирование строки для отвлечения внимания
    strcpy(processed_message, initial_message);
    printf("%s", processed_message);
    printf("Welcome to the enhanced data processing program!\n");
    printf("Please enter your data: ");

    read_data();

    // Вызов функции обработки данных пользователя
    process_user_data();

    printf("Data processing completed!\n");
    return 0;
}
