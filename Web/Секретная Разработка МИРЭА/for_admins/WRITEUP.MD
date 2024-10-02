# Инструкция по Настройке Tampermonkey для Mirea Browser

Следуйте приведённым ниже шагам, чтобы настроить ваш браузер для работы с сайтом, который поддерживает только **Mirea Browser**.

## Шаг 1: Установка Tampermonkey

При открытии сайта вы получите сообщение о том, что он поддерживает только **Mirea Browser**. Для обхода этого ограничения необходимо установить расширение Tampermonkey.

1. Перейдите в магазин расширений вашего браузера.
2. Найдите и установите [Tampermonkey](https://www.tampermonkey.net/).
3. После установки иконка Tampermonkey появится в панели инструментов вашего браузера.

## Шаг 2: Создание Пользовательского Скрипта

Желательно в разедле сети выключить кэш браузера

После установки Tampermonkey необходимо создать скрипт, который изменит информацию о вашем браузере, заставив сайт думать, что вы используете **Mirea Browser**.

1. Кликните на иконку Tampermonkey в панели инструментов.
2. Выберите **"Создать новый скрипт"**.
3. Замените содержимое редактора на следующий код:

    ```javascript
    // ==UserScript==
    // @name         Spoof Mirea Browser
    // @namespace    http://tampermonkey.net/
    // @version      1.0
    // @description  Изменяет информацию о браузере на Mirea Browser
    // @match        *://*/*
    // @grant        none
    // ==/UserScript==

    (function() {
        'use strict';

        Object.defineProperty(navigator, 'userAgent', {
            get: function () { return 'Mirea Browser'; },
            configurable: true
        });

        Object.defineProperty(navigator, 'appName', {
            get: function () { return 'Mirea Browser'; },
            configurable: true
        });

        Object.defineProperty(navigator, 'appVersion', {
            get: function () { return 'Mirea Browser Version 1.0'; },
            configurable: true
        });

        Object.defineProperty(navigator, 'platform', {
            get: function () { return 'Mirea Platform'; },
            configurable: true
        });
    })();
    ```

4. Сохраните скрипт, нажав **"Файл"** > **"Сохранить"** или используя сочетание клавиш **Ctrl+S**.

## Шаг 3: Активация Скрипта и Перезагрузка Страницы

1. Убедитесь, что созданный скрипт **включён** в Tampermonkey.
2. Перезагрузите страницу сайта, который изначально требовал **Mirea Browser**.
3. Теперь сайт должен распознавать ваш браузер как **Mirea Browser** и работать корректно.

