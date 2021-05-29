from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import escape

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello Totoro!@!</h1><img src="http://helloflask.com/totoro.gif">'

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