from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import Config
from flask import Flask


app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'auth_bp.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'You need to login to do that.'

mail = Mail(app)

from app.auth.routes import auth_bp
from app.main.routes import main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
