import sys, os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(os.path.dirname(app.root_path), 'data.db')  # connect to SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@127.0.0.1/flask_db' #connect to MySql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

app.config['SECRET_KEY'] = 'dev' #好像必须要得有这个，用来存flash()的内容
#flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，
# 它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥：
# 这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里。

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return {'user': user}

from watchlist import views, errors, commands