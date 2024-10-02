import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data['expression']
        result = eval(expression)
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'result': 'Error'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0")