import zipfile
import os
import shutil

def extract_file_from_nested_archives(start_archive, output_file):
    current_archive = start_archive
    temp_dir = "temp_extract"

    # Создаем временную директорию для извлечения, если её нет
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    while True:
        # Открываем текущий архив
        with zipfile.ZipFile(current_archive, 'r') as zipf:
            # Предполагаем, что в архиве один файл
            file_name = zipf.namelist()[0]
            
            # Извлекаем файл во временную папку
            zipf.extract(file_name, temp_dir)
            extracted_file = os.path.join(temp_dir, file_name)
            print(f"Извлечен {file_name} из {current_archive}")
            
            # Проверяем, является ли извлеченный файл еще одним архивом
            if file_name.endswith('.zip'):
                # Если это архив, продолжаем извлечение
                current_archive = extracted_file
            else:
                # Копируем конечный файл в нужное место
                shutil.move(extracted_file, output_file)
                print(f"Исходный файл {file_name} извлечен и сохранен как {output_file}")
                break

    # Удаляем временную директорию
    shutil.rmtree(temp_dir)

# Использование функции
start_archive = "flag2000.zip"  # Укажите начальный архив
output_file = "final_extracted_file.txt"  # Укажите путь для сохранения конечного файла
extract_file_from_nested_archives(start_archive, output_file)
