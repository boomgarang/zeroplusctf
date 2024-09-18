from flask import Flask, request, render_template, session, redirect, url_for
from lxml import etree  # Уязвимый парсер lxml
import os

app = Flask(__name__)
app.secret_key = 'abobahueba'  # Необходимо для использования сессий

# Отображение index.html на маршруте '/'
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            # Получаем XML из запроса
            xml_data = request.data
            # Устанавливаем путь для поиска внешних сущностей
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            # Параметры для парсера
            parser = etree.XMLParser(resolve_entities=True)  # Разрешаем внешние сущности и DTD
            
            # Настройка для обработки относительных путей
            etree.set_default_parser(parser)
            
            # Парсинг XML данных (уязвимый к XXE)
            tree = etree.fromstring(xml_data, parser)
            
            # Извлечение данных из XML
            first = tree.find('first').text
            last = tree.find('last').text
            email = tree.find('email').text
            mobile = tree.find('mobile').text
            gender = tree.find('gender').text
            app.logger.info(first)
            
            # Сохраняем данные в сессии
            session['first'] = first
            session['last'] = last
            session['email'] = email
            session['mobile'] = mobile
            session['gender'] = gender

            # Перенаправление на страницу профиля
            return redirect(url_for('profile'))
    
    except Exception as e:
        return str(e), 400

@app.route('/profile')
def profile():
    # Получаем данные из сессии
    first = session.get('first')
    last = session.get('last')
    email = session.get('email')
    mobile = session.get('mobile')
    gender = session.get('gender')
    
    # Отображаем страницу profile.html с переданными данными
    return render_template('profile.html', first=first, last=last, email=email, mobile=mobile, gender=gender)

# Запуск Flask-сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
