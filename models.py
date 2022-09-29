from flask_sqlalchemy import SQLAlchemy



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
