# coding: UTF-8

import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#データベース接続など
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:256UniA:fsP4@localhost/スケジュール"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Root.123@localhost/スケジュール"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
#ログインしてないときに飛ぶURL
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login_screen")

#データベースモデル定義
class Schedule(db.Model):
    __tablename__="スケジュール"
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    date = db.Column(db.DATE)
    starttime = db.Column(db.TIME)
    endtime = db.Column(db.TIME)
    title = db.Column(db.VARCHAR(255))
    content = db.Column(db.TEXT)
    user_id = db.Column(db.INT, db.ForeignKey("ユーザー.id"))

class User(db.Model, UserMixin):
    __tablename__="ユーザー"
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    user_name = db.Column(db.VARCHAR(32))
    user_password = db.Column(db.VARCHAR(100))
    
    schedule = db.relationship("Schedule", backref = db.backref("ユーザー"), lazy = True)
    


@app.route("/")
def top():
    title = "スケジュールアプリ"
    return render_template("toppage.html", title = title)

#ログイン処理
@app.route("/signup_screen")
def signup_screen():
    title = "ユーザの新規登録"
    return render_template("signup.html", title = title)

@app.route("/signup", methods=["POST"])
def signup():
    user_name = request.form.get("user_name")
    user_password = request.form.get("user_password")

    #ユーザ名が存在するかどうか調べる
    check_user = User.query.filter_by(user_name=user_name).first()
    if check_user != None:
        flash("ユーザ「" + user_name + "」は既に存在します。")
        return redirect("/signup_screen")

    #ユーザを作成する
    user = User()
    user.user_name = user_name
    user.user_password = generate_password_hash(user_password, method="sha256")

    db.session.add(user)
    db.session.commit()
    
    return redirect("/login_screen")

@app.route("/login_screen")
def login_screen():
    title = "ログイン"
    return render_template("login.html", title = title)
        
@app.route("/login", methods=["GET", "POST"])
def login():
    user_name = request.form.get("user_name")
    user_password = request.form.get("user_password")
        
    # Userテーブルからusernameに一致するユーザを取得
    user = User.query.filter_by(user_name=user_name).first()
    if user == None:
        flash("ユーザ「" + user_name + "」は存在しません")
        return redirect("/login_screen")
        
    if check_password_hash(user.user_password, user_password):
        login_user(user)
        return redirect("/home")
    else:
        flash("パスワードが違います")
        return redirect("/login_screen")



#本体処理
@app.route("/home")
@login_required
def home():
    title       = "さんのホーム"
    posts       = Schedule.query.all()
    user_name   = current_user.user_name #User.query.get(1)
    title       = user_name + title
    return render_template("home.html", title = title, posts = posts)

@app.route("/new")
@login_required
def new():
    title = "新規スケジュール"
    return render_template("new.html", title = title)
    
@app.route("/create", methods = ["POST"])
@login_required
def create():
    schedule    = Schedule()
    schedule.user_id    = current_user.id
    schedule.title      = request.form["title"]
    schedule.date       = request.form["date"]
    schedule.starttime  = request.form["start_time"]
    schedule.endtime    = request.form["end_time"]
    schedule.content    = request.form["content"]
    db.session.add(schedule)
    db.session.commit()

    post = Schedule.query.get(schedule.id)
    title = "タイトル名をここに入力"
    return render_template("show.html", title = title, post = post, id = 0)

@app.route("/show/<int:id>")
@login_required
def show(id):
    post = Schedule.query.get(id)
    title = "スケジュール「" + post.title + "」"
    return render_template("show.html", title = title, post = post, id = id)

@app.route("/edit/<int:id>")
@login_required
def edit(id):
    post = Schedule.query.get(id)
    title = "スケジュールを編集"
    return render_template("edit.html", title = title, post = post, id = id)

@app.route("/update/<int:id>", methods = ["POST"])
@login_required
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
    return render_template("show.html", title = title, post = post, id = 0)

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    schedule = Schedule.query.get(id)
    db.session.delete(schedule)
    db.session.commit()

    title = "ホーム"
    posts = Schedule.query.all()
    return render_template("home.html", title = title, posts = posts)

#ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

## おまじない
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)