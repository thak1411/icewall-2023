from flask import Flask, request, render_template, redirect, session
from dotenv import dotenv_values
from models import db, User
from pathlib import Path

import os

app = Flask(__name__)

@app.route('/')
def hello():
    if 'username' not in session:
        return redirect('/login/')
    else:
        username = session['username']
        return 'Hello, ' + username

@app.route('/signup/', methods= ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not (username):
            return '사용자 이름이 입력되지 않았습니다'
        else:
            usertable=User()
            usertable.username = username
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()
            return '회원가입 성공'
    
    else:
        return render_template('signup.html')

@app.route('/login/', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not (username and password):
            return '아이디 혹은 패스워드를 입력해 주세요.'
        else:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                session['username'] = username
                return redirect('/')
            else:
                return '아이디 혹은 패스워드가 올바르지 않습니다.'
    else:
        return render_template('login.html')

def main():
    dotenv_path = Path(__file__).parent.parent / '.env'
    config = dotenv_values(dotenv_path)

    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        dbfile = os.path.join(basedir, 'db.sqlite')
        app.config['SECRET_KEY'] = config.get('SECRET_KEY', 'ICEWALL')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.app = app
        db.create_all()

        app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()