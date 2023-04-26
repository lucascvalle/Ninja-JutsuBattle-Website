from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os
import sqlalchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = '7320fc257bab603bdb7834280f67794e'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ninjajutsubattle.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from ninjajutsubattle import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not engine.has_table("user"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Database created')
else:
    print('Database already exists')


from ninjajutsubattle import routes
