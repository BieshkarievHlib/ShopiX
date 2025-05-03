from proj import db
from datetime import datetime
from pytz import timezone

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    delivery = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Kyiv')))
    #TODO: add optional comment
    
    products = db.relationship('OrderToProduct', backref='order', lazy=True)

class OrderToProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer, default=1, nullable=False)