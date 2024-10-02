## **"Фортуна любит смелых"**
Добро пожаловать в мир удачи и риска! На вашем игровом счёте уже есть 1000, но для получения флага нужно гораздо больше. Удастся ли вам найти способ увеличить баланс до 10000, не полагаясь только на фортуну? Пора испытать свою смекалку и разобраться, как обойти систему.

Время — деньги, дерзайте!

http://91.77.163.113:15000

## WRITEUP

#### Шаг 1: Исследуем запросы

Запускаем спин на слоте и смотрим, какие запросы отправляются на сервер. Замечаем, что вместе с числами (вероятно, связанными с результатами спина) отправляется какой-то хеш. Этот хеш, вероятно, используется для проверки подлинности запроса. Нам нужно понять, как его правильно сгенерировать.

#### Шаг 2: Ищем функцию генерации хеша

Открываем файл `scripts.js`, который содержит клиентскую логику. После поиска находим функцию под названием `generateHash`. В этой функции числа хешируются: сначала через SHA1, затем два раза через MD5.

#### Шаг 3: Генерация хеша

Теперь у нас есть понимание, как генерируется хеш. Используем сайт [CyberChef](https://cyberchef.org) для генерации хеша по той же схеме:

1.  Сначала применяем SHA1.
2.  Потом два раза MD5.
[Пример](https://cyberchef.org/#recipe=SHA1(80)MD5()MD5()&input=Nzc3)
#### Шаг 4: Подбираем число и хеш

Используя функцию генерации хеша, вводим подходящее число и создаем соответствующий хеш. Теперь мы можем отправлять запросы на сервер с правильным хешем и числом

#### Шаг 5: Выполняем запросы

Отправляем запросы с корректным числом и хешем до тех пор, пока на нашем балансе не накопится 10000$.

#### Шаг 6: Получаем флаг

Как только баланс достигает 10000$, мы можем получить флаг.