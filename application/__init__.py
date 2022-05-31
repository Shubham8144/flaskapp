
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SECRET_KEY'] = 'a744b12533e8ccf6f3171883e13cdc3b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root#123@localhost:3306/flask_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:Test#123@localhost/tflask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes