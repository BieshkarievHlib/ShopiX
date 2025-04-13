from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0317e094110acd8ab357a731caf393287120b76779f2acf20e2438fdca88cb62' #TODO: Оновити та перенести в .env, коли додам .gitignore

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from . import routes
