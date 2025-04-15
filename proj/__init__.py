from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from markupsafe import Markup

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0317e094110acd8ab357a731caf393287120b76779f2acf20e2438fdca88cb62' #TODO: Оновити та перенести в .env, коли додам .gitignore
# VULNERABILITY: Hardcoded Secret Key
# - Secret key is hardcoded in the source code
# - Same key used in all environments
# - Key is committed to version control
# - Should use environment variables or config files
# - Should use different keys for different environments

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# VULNERABILITY: Session Security
# - No session timeout configuration
# - No secure flag on session cookies
# - No HTTP-only flag on session cookies
# - Should implement proper session security measures

def nl2br(value):
    return Markup(value.replace('\n', '<br>'))

app.jinja_env.filters['nl2br'] = nl2br

from . import routes
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
