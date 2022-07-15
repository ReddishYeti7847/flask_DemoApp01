import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

#データベース接続など
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:256UniA:fsP4@localhost/スケジュール"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

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
    return render_template("toppage.html", messeage = title)

#ログイン処理
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        user = User()
        password = request.form.get("user_password")
        user.user_name = request.form.get("user_name")
        user.user_password = generate_password_hash(password, method="sha256")
        # Userのインスタンスを作成
#        user = User(user_name=user_name, user_password=generate_password_hash(user_password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect("/login_screen")
    else:
        return render_template("signup.html")
        
@app.route("/login_screen")
def login_screen():
    title = "ログイン"
    return render_template("login.html", messeage = title)
        
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        
        # Userテーブルからusernameに一致するユーザを取得
        #user = User.query.filter_by(user_name=user_name).first()
        user = User.query.filter_by(user_name=user_name).first()
        
        if check_password_hash(user.user_password, user_password):
            login_user(user)
            return redirect("/home")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")



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