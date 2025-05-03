from flask import render_template, url_for, redirect, request

from proj.admin import admin
from proj import db
from proj.cart.models import Order

@admin.route('/')
def index():
    orders = Order.query.filter_by()
    return render_template('admin/orderlist.html', orders=orders)

@admin.route('/orders/<int:order_id>/update', methods=['POST'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status:
        order.status = new_status
        db.session.commit()
    return redirect(url_for('admin.index'))

@admin.route('orders/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('admin.index'))