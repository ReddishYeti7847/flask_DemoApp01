import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#データベース接続など
app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:256UniA:fsP4@localhost/スケジュール'
db = SQLAlchemy(app)

#データベースモデル定義
class Schedule(db.Model):
    __tablename__='スケジュール'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    date = db.Column(db.DATE)
    starttime = db.Column(db.TIME)
    endtime = db.Column(db.TIME)
    title = db.Column(db.VARCHAR(255))
    content = db.Column(db.TEXT)
    user_id = db.Column(db.INT, db.ForeignKey('ユーザー.id'))

class User(db.Model):
    __tablename__='ユーザー'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    user_name = db.Column(db.VARCHAR(32))
    user_password = db.Column(db.VARCHAR(32))
    
    schedule = db.relationship('Schedule', backref = db.backref('ユーザー'), lazy = True)
    



#ログイン処理
@app.route("/")
def login():
    title = "さんのホーム"
    posts = Schedule.query.all()
    users = User.query.get(1)
    title = users.user_name + title
    return render_template("home.html", messeage = title, posts = posts)

## おまじない
if __name__ == "__main__":
    app.run(debug=True, port = 8080)