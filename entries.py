import os
from flask import Flask, render_template, request, redirect, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

entry = Blueprint("entry", __name__)

@entry.route("/")
def top():
    title = "スケジュールアプリ"
    return render_template("toppage.html", title = title)

#ログイン処理
@entry.route("/signup_screen")
def signup_screen():
    title = "ユーザの新規登録"
    return render_template("signup.html", title = title)

@entry.route("/signup", methods=["POST"])
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

@entry.route("/login_screen")
def login_screen():
    title = "ログイン"
    return render_template("login.html", title = title)
        
@entry.route("/login", methods=["GET", "POST"])
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