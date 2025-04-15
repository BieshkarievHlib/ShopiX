from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from proj import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'Product {self.id} named {self.name}'

class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'ProductType {self.name}'
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(64), unique=False, nullable=False)
    surname = db.Column(db.String(64), unique=False, nullable=False)

    def check_password(self, password):
        return self.password == password  #TODO: Вразливість: додати хешування  
        # VULNERABILITY: Plain text password storage and comparison
        # - Passwords are stored in plain text in the database
        # - No password hashing or salting
        # - Vulnerable to database leaks and rainbow table attacks
        # - Should use proper password hashing (e.g., bcrypt, Argon2)

    def __repr__(self):
        return f'User {self.username}"\n\tName: {self.name} {self.surname}\n\tE-mail: {self.email}'
