from proj import db

class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'ProductType {self.name}'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=True, default=0.01) #TODO: set nullable=False after a wipe-out

    orders = db.relationship('OrderToProduct', backref='product', lazy=True)

    def __repr__(self):
        return f'Product {self.id} named {self.name}'
