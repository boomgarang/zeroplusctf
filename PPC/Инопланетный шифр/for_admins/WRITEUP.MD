# Дешифратор QR-кодов для поиска CTF флагов

Этот скрипт предназначен для декодирования QR-кодов из указанной папки и поиска внутри декодированных данных обёртки с флагом CTF.

## Требования

Для запуска этого скрипта необходимо установить следующие библиотеки:

- [Pillow](https://python-pillow.org/) (`PIL`)
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [tqdm](https://tqdm.github.io/)

Установите их с помощью `pip`:

```bash
pip install Pillow pyzbar tqdm
```
```python
import os
from PIL import Image
from pyzbar.pyzbar import decode
import json
from tqdm import tqdm  # Импортируем tqdm для индикатора прогресса

# Папка с QR-кодами
input_folder = "qr_codes"
output_file = "decoded_qr_codes.json"

# Строка для поиска
search_string = "KpkCTF"

# Функция для чтения всех QR-кодов и записи результатов в JSON
def decode_qr_codes():
    decoded_data_list = []

    # Получаем список файлов с поддерживаемыми расширениями
    supported_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_extensions)]

    if not files:
        print(f"В папке '{input_folder}' нет файлов с поддерживаемыми расширениями: {supported_extensions}")
        return

    # Используем tqdm для отображения прогресса
    for filename in tqdm(files, desc="Обработка QR-кодов", unit="файл"):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path)
        except Exception as e:
            print(f"\nНе удалось открыть изображение {filename}: {e}")
            continue

        decoded_data = decode(img)

        if not decoded_data:
            print(f"\nQR-код не найден в файле {filename}.")
            continue

        for obj in decoded_data:
            try:
                decoded_text = obj.data.decode("utf-8")
            except UnicodeDecodeError:
                print(f"\nНе удалось декодировать данные из {filename}.")
                continue

            decoded_entry = {
                "filename": filename,
                "text": decoded_text
            }
            decoded_data_list.append(decoded_entry)

            # Проверка на наличие искомой строки
            if search_string in decoded_text:
                print(f"\nНайдено в {filename}: {decoded_text}")

    # Сохранение результатов в JSON файл
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(decoded_data_list, f, ensure_ascii=False, indent=4)
        print(f"\nДешифрованные данные сохранены в '{output_file}'")
    except Exception as e:
        print(f"\nНе удалось сохранить JSON файл: {e}")

# Декодирование QR-кодов и запись в JSON
if __name__ == "__main__":
    decode_qr_codes()
```