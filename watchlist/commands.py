import click

from watchlist import app, db
from watchlist.models import User, Movie

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
    click.echo('Done.')


# 自定义指令add user
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    db.create_all()
    
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('Done.')