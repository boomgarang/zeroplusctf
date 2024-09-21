# Описани

Открываем архив, в нем архив, и файл с паролем. Значит, нужно извлечь пароль из файл, открыть с его помощью архив и повторить это действие 1000 раз.

```python
import io
import zipfile
import pyzipper

# Функция для извлечения архивов из памяти
def extract_archives_in_memory(starting_archive, total_archives):
    current_archive = starting_archive
    next_password = None

    for i in range(total_archives, 0, -1):
        # Проверяем, если это самый внешний архив (без пароля)
        if i == total_archives:
            with zipfile.ZipFile(current_archive, 'r') as zipf:
                print(f"Извлечен архив {current_archive} без пароля")

                # Ищем архив следующего уровня и файл с паролем для него
                archive_name = None
                password_file = None
                for name in zipf.namelist():
                    if name.startswith('archive_'):
                        archive_name = name
                    if name.startswith('password_for_archive_'):
                        password_file = name

                if archive_name:
                    # Извлекаем следующий архив в память
                    next_archive_data = zipf.read(archive_name)
                    next_archive = io.BytesIO(next_archive_data)
                else:
                    next_archive = None

                # Извлекаем файл с паролем для следующего архива
                if password_file:
                    next_password = zipf.read(password_file).decode('utf-8').strip()
                    print(f"Пароль для архива {i-1}: {next_password}")
        else:
            # Для всех остальных архивов требуется пароль
            with pyzipper.AESZipFile(current_archive, 'r') as zipf:
                zipf.setpassword(next_password.encode())
                print(f"Извлечен архив {current_archive} с паролем")

                # Ищем архив следующего уровня и файл с паролем для него
                archive_name = None
                password_file = None
                for name in zipf.namelist():
                    if name.startswith('archive_'):
                        archive_name = name
                    if name.startswith('password_for_archive_'):
                        password_file = name

                if archive_name:
                    # Извлекаем следующий архив в память
                    next_archive_data = zipf.read(archive_name)
                    next_archive = io.BytesIO(next_archive_data)
                else:
                    next_archive = None

                # Извлекаем файл с паролем для следующего архива
                if password_file:
                    next_password = zipf.read(password_file).decode('utf-8').strip()
                    print(f"Пароль для архива {i-1}: {next_password}")

        # Если это архив 1, его больше нет смысла извлекать, но пароль нужен
        if i == 1:
            with pyzipper.AESZipFile(current_archive, 'r') as final_zip:
                final_zip.setpassword(next_password.encode())
                print(f"Извлекаем последний архив {current_archive} с паролем")
                final_zip.extractall("final_extracted_data")
            break

        # Обновляем текущий архив на извлеченный архив в памяти, если он есть
        current_archive = next_archive

    print("Все архивы успешно извлечены.")

# Использование функции
with open("archive_1000.zip", "rb") as f:
    starting_archive = io.BytesIO(f.read())  # Загружаем самый внешний архив в память

total_archives = 1000  # Укажите общее количество уровней архивов
extract_archives_in_memory(starting_archive, total_archives)

```