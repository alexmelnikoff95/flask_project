import os
import sqlite3

from flask import Flask, render_template, g, url_for, request, flash, abort

from FDataBase import FDataBase

DATABASE = '/tmp/flask_bd.db'
DEBUG = True
SECRET_KEY = 'ASFDFD123'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_bd')))

name = [
    {'name': 'profile', 'url': '/profile'},
    {'name': 'auth', 'url': '/login'},
    {'name': 'обратная связь', 'url': '/contact'},
]


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    url_for('index')
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', context=dbase.get_name(), posts=dbase.getPostAncone())


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    url_for('addPost')
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('ошибка добаления статьи', category='error')
            else:
                flash('статья добавлена', category='ok')
        else:
            flash('ошибка добавления статьи', category='error')
    return render_template('add_post.html', context=dbase.get_name(), title='Добавление статьи')


@app.route('/post/<int:id_post>')
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', context=dbase.get_name(), title=title, post=post)


@app.do_teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True, )
