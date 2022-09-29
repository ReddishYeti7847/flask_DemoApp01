import os
from flask import Flask, render_template, request, redirect, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#データベース接続など
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:256UniA:fsP4@localhost/スケジュール"

db = SQLAlchemy()

#ログイン処理の初期化
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
#ログインしてないときに飛ぶURL
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login_screen")



#ログイン処理
# from ファイル名            import 参照するファイルで定義した変数名　　　または
# from フォルダ名.ファイル名 import 参照するファイルで定義した変数名
# https://hogetech.info/programming/python/flask/blueprint　の記事を参考
from entries import entry
app.register_blueprint(entry)



#本体処理
from views import view
app.register_blueprint(view)

## おまじない
if __name__ == "__main__":
    app.run(debug=True, port = 8080)