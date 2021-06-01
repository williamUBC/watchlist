from flask import Flask, render_template
from flask.helpers import url_for
from werkzeug.utils import escape
from flask_sqlalchemy import SQLAlchemy

import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)

# 自定义指令，用于初始化db文件
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        click.echo('Drop all database.')
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
# 在terminal中执行flask initdb 或 flask initdb --drop使用，注意不是在flask shell中执行

# 自定义指令，用于向数据库添加测试数据
@app.cli.command()
def forge():
    click.echo('Inputing data to db...')
    name = 'William'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)    
    db.session.add(user)

    for m in movies:
        db.session.add(Movie(title=m['title'], year=m['year']))
    
    db.session.commit()
    click.echo('Finish!')

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db') #connect to SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@127.0.0.1/flask_db' #connect to MySql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return "User name is {user_name}".format(user_name=escape(name))
    '''
     用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用
      Flask 提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。
      这样在返回响应时浏览器就不会把它们当做代码执行。
    '''

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='zw'))
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'