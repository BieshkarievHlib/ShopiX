from flask import render_template, url_for, redirect

from proj.cart.models import Order

def orderlist():
    orders = Order.query.all()
    return render_template('admin/orderlist.html', orders=orders)