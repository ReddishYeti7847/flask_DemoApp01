import os
from flask import Flask, render_template, request, redirect, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

view = Blueprint("view", __name__)



#本体処理
@view.route("/home")
@login_required
def home():
    title       = "さんのホーム"
    posts       = Schedule.query.all()
    user_name   = current_user.user_name #User.query.get(1)
    title       = user_name + title
    return render_template("home.html", title = title, posts = posts)

@view.route("/new")
@login_required
def new():
    title = "新規スケジュール"
    return render_template("new.html", title = title)
    
@view.route("/create", methods = ["POST"])
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

@view.route("/show/<int:id>")
@login_required
def show(id):
    post = Schedule.query.get(id)
    title = "スケジュール「" + post.title + "」"
    return render_template("show.html", title = title, post = post, id = id)

@view.route("/edit/<int:id>")
@login_required
def edit(id):
    post = Schedule.query.get(id)
    title = "スケジュールを編集"
    return render_template("edit.html", title = title, post = post, id = id)

@view.route("/update/<int:id>", methods = ["POST"])
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

@view.route("/delete/<int:id>")
@login_required
def delete(id):
    schedule = Schedule.query.get(id)
    db.session.delete(schedule)
    db.session.commit()

    title = "ホーム"
    posts = Schedule.query.all()
    return render_template("home.html", title = title, posts = posts)

#ログアウト
@view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')