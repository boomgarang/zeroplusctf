1. Для решения задания нужно проанализировать логи и найти необычные из них
2. Этот код выполняет задачу.

```python
import sys

def is_standard_log(line):
    """
    Проверяет, содержит ли строка стандартный уровень логирования.
    """
    standard_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
    for level in standard_levels:
        if f'] {level} ' in line:
            return True
    return False

def extract_non_standard_lines(filename='server.log'):
    """
    Извлекает и возвращает строки, которые не содержат стандартных уровней логирования.
    """
    non_standard_lines = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if not is_standard_log(line):
                    non_standard_lines.append(line.strip())
    except FileNotFoundError:
        print(f'Файл "{filename}" не найден.')
        sys.exit(1)
    
    return non_standard_lines



def main():
    """
    Основная функция для поиска флага в лог-файле.
    """
    # Получение имени файла из аргументов командной строки
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'server.log'
    
    # Извлечение не стандартных строк
    non_standard_lines = extract_non_standard_lines(filename)
    
    # Вывод найденных строк
    print("Найденные строки без стандартных уровней логирования:")
    for line in non_standard_lines:
        print(line)
    


if __name__ == "__main__":
    main()

```