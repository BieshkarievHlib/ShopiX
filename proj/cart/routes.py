from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user

from pytz import timezone
from datetime import datetime

from proj import db
from proj.cart import cart
from proj.cart.models import Order, OrderToProduct
from proj.cart.forms import OrderForm
from proj.products.models import Product

@cart.context_processor
def utility_processor():
    def get_product(product_id):
        return Product.query.get(int(product_id))
    return {'get_product': get_product}

@cart.route('/', methods=['GET'])
def index():
    if 'cart' not in session:
        session['cart'] = []
    
    cart_items = []
    total = 0
    
    for item in session['cart']:
        product = Product.query.get(item['id'])
        if product:
            cart_items.append({
                'product': product,
                'quantity': item['quantity']
            })
            total += product.price * int(item['quantity'])
    
    return render_template('cart/cart.html', cart_items=cart_items, total=total)

@cart.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'cart' not in session or id >= len(session['cart']):
        return redirect(url_for('cart.index'))
    
    quantity = int(request.form.get('quantity', 1))
    if quantity > 0:
        session['cart'][id]['quantity'] = quantity
        session.modified = True
    
    return redirect(url_for('cart.index'))

@cart.route('/remove/<int:id>')
def remove(id):
    if 'cart' in session and id < len(session['cart']):
        session['cart'].pop(id)
        session.modified = True

    return redirect(url_for('cart.index'))

@cart.route('/clear')
def clear():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('cart.index'))

@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    #TODO: add checkout for anonymous users
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('products.index'))

    form = OrderForm()

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            delivery=form.delivery.data,
            status='pending',
            created_at=datetime.now(timezone('Europe/Kyiv'))
        )

        db.session.add(order)
        db.session.flush()  

        for item in session['cart']:
            product = Product.query.get(item['id'])
            if product and product.in_stock >= int(item['quantity']):
                order_item = OrderToProduct(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item['quantity']
                )
                db.session.add(order_item)
                
                product.in_stock -= int(item['quantity'])
                #VULNERABILITY: denial of service
                # - Vulnerable to DoS attacks 
                # - Allows user (specifically anonymous) to decrement product.in_stock 'till it reaches 0.
                # - Restrictions implementation/more complex transaction system is recommended.

            else:
                return redirect(url_for('cart.index'))
        
        db.session.commit()
        session['cart'] = []
        session.modified = True
        
        return redirect(url_for('products.index'))
        
    return render_template('cart/checkout.html', form=form, cart=session['cart'])
