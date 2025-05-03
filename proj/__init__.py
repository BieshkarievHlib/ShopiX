from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_principal import Principal, Identity, UserNeed, RoleNeed, identity_loaded
from markupsafe import Markup

# Create extensions before app initialization
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# VULNERABILITY: Session Security
# - No session timeout configuration
# - No secure flag on session cookies
# - No HTTP-only flag on session cookies
# - Should implement proper session security measures

def nl2br(value):
    return Markup(value.replace('\n', '<br>'))

def create_app():
    app = Flask(__name__)
    principals = Principal(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '0317e094110acd8ab357a731caf393287120b76779f2acf20e2438fdca88cb62' #TODO: Оновити та перенести в .env, коли додам .gitignore
    # VULNERABILITY: Hardcoded Secret Key
    # - Secret key is hardcoded in the source code
    # - Same key used in all environments
    # - Key is committed to version control
    # - Should use environment variables or config files
    # - Should use different keys for different environments
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    principals.init_app(app)
    
    app.jinja_env.filters['nl2br'] = nl2br
    
    from proj.auth import auth as auth_blueprint
    from proj.products import products as products_blueprint
    from proj.cart import cart as cart_blueprint
    from proj.admin import admin as admin_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(admin_blueprint)
    
    # Root route
    @app.route('/')
    def index():
        return redirect(url_for('products.index'))
    
    return app

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from proj.auth.models import User
    return User.query.get(int(user_id))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if not current_user.is_anonymous:
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(RoleNeed(current_user.role.name))