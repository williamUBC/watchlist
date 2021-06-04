from werkzeug.utils import escape

from flask import redirect, request, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required

from watchlist import app, db
from watchlist.models import Movie, User


@app.route('/', methods=['GET', 'POST'])
def index():
    #user = User.query.first()
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页

        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return "User name is {user_name}".format(user_name=escape(name))
    '''
     用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用
      Flask 提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。
      这样在返回响应时浏览器就不会把它们当做代码执行。
    '''


# @app.route('/test')
# def test_url_for():
#     # print(url_for('hello'))
#     print(url_for('user_page', name='wow'))
#     print(url_for('test_url_for'))  # 输出：/test
#     # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
#     print(url_for('test_url_for', num=2))  # 输出：/test?num=2

#     print(url_for('edit', movie_id=1))
#     return 'Test page'


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if user.username == username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')
