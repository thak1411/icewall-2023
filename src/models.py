from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    _tablename = 'user' #테이블 이름

    id = db.Column(db.Integer, primary_key=True) # 자동으로 증가하는 User 모델의 기본 키 
    username = db.Column (db.String (100), unique=True, nullable=False) # 같은 값 저장 X, 빈 값 X
    password = db.Column(db.String (20), nullable=False) # 빈값 X