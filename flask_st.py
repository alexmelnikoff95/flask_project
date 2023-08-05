from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ASFDFD123'

name = [
    {'name': 'profile', 'url': '/profile'},
    {'name': 'auth', 'url': '/login'},
    {'name': 'обратная связь', 'url': '/contact'},
]


@app.route('/')
def index():
    url_for('index')
    return render_template('index.html', context=name)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'пользователь {username}'


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['first_name']) > 2:
            flash('сообщение отправлено', category='ok')
        else:
            flash('ошибка отправки', category='error')
    return render_template('contact.html', title='обратная связь', context=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    print(session)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'alex' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', context=name)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', context=name), 404


if __name__ == '__main__':
    app.run(debug=True, )
