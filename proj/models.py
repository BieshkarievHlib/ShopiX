from proj import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    in_stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'Product {self.id} named {self.name}'

class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'ProductType {self.name}'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f'User {self.username}"\n\tName: {self.name} {self.surname}\n\tE-mail: {self.email}'
