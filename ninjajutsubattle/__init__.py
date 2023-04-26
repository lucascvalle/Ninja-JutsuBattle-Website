from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = '7320fc257bab603bdb7834280f67794e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ninjajutsubattle.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from ninjajutsubattle import routes