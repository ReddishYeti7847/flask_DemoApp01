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



#本体処理
@app.route("/home")
def home():
    title = "さんのホーム"
    posts = Schedule.query.all()
    users = User.query.get(1)
    title = users.user_name + title
    return render_template("home.html", messeage = title, posts = posts)

@app.route("/new")
def new():
    title = "新規スケジュール"
    return render_template("new.html", messeage = title)
    
@app.route("/create", methods = ["POST"])
def create():
    schedule = Schedule()
    schedule.user_id = 1
    schedule.title = request.form["title"]
    schedule.date = request.form["date"]
    schedule.starttime = request.form["start_time"]
    schedule.endtime = request.form["end_time"]
    schedule.content = request.form["content"]
    db.session.add(schedule)
    db.session.commit()

    post = Schedule.query.get(schedule.id)
    title = "タイトル名をここに入力"
    return render_template("show.html", messeage = title, post = post, id = 0)

@app.route("/show/<int:id>")
def show(id):
    post = Schedule.query.get(id)
    title = "タイトル名をここに入力"
    return render_template("show.html", messeage = title, post = post, id = id)

@app.route("/edit/<int:id>")
def edit(id):
    post = Schedule.query.get(id)
    title = "スケジュールを編集"
    return render_template("edit.html", messeage = title, post = post, id = id)

@app.route("/update/<int:id>", methods = ["POST"])
def update(id):
    schedule = Schedule.query.get(id)
    schedule.user_id = 1
    schedule.title = request.form["title"]
    schedule.date = request.form["date"]
    schedule.starttime = request.form["start_time"]
    schedule.endtime = request.form["end_time"]
    schedule.content = request.form["content"]
    db.session.commit()

    post = Schedule.query.get(schedule.id)
    title = "タイトル名をここに入力"
    return render_template("show.html", messeage = title, post = post, id = 0)

@app.route("/delete/<int:id>")
def delete(id):
    schedule = Schedule.query.get(id)
    db.session.delete(schedule)
    db.session.commit()

    title = "ホーム"
    posts = Schedule.query.all()
    return render_template("home.html", messeage = title, posts = posts)

## おまじない
if __name__ == "__main__":
    app.run(debug=True, port = 8080)