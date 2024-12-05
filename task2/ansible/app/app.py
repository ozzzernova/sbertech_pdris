from flask import Flask, render_template, redirect, url_for, request
from src.random import hash_function

app = Flask(__name__)
action = word = ""
tmp = sign = change = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/game/random', methods=['GET'])
def random():
    return render_template('random.html')


@app.route('/game/result', methods=['POST'])
def result():
    global word, action, sign, change
    text = request.form['text']
    word = text[::]
    action, tmp, sign, change = hash_function(text)
    return render_template('result.html', word=word, action=action, sign=sign, change=change, tmp=tmp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
