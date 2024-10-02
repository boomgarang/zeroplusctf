import re
import socket
import time

# Функция для вычисления результата примера
def solve_task(task):
    # Используем регулярное выражение для извлечения чисел и операции
    match = re.search(r'(\d+)\s*([\+\*])\s*(\d+)', task)
    if not match:
        return None  # если формат задачи некорректен
    
    num1 = int(match.group(1))
    operation = match.group(2)
    num2 = int(match.group(3))
    
    if operation == '+':
        return num1 + num2
    elif operation == '*':
        return num1 * num2
    else:
        return None  # неизвестная операция

# Подключение к серверу через socket
def math_game_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        buffer = ""
        
        while True:
            # Получаем данные от сервера
            data = s.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            
            # Выводим полученные данные (для отладки)
            print(buffer)
            
            # Поиск задач в полученном буфере
            task_lines = buffer.splitlines()
            for line in task_lines:
                if "Solve:" in line:
                    result = solve_task(line)
                    if result is not None:
                        # Отправляем результат обратно на сервер
                        s.sendall(f"{result}\n".encode('utf-8'))
                        print(f"Sent answer: {result}")
            
            # Очищаем буфер, чтобы не дублировать данные
            buffer = ""

if __name__ == "__main__":
    host = "localhost"  # Адрес сервера
    port = 12345        # Порт сервера
    
    # Подключаемся и решаем задачи
    math_game_client(host, port)
