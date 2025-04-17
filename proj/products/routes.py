from flask import render_template, redirect, url_for, request, session
from flask_login import login_required

from proj import db
from proj.products import products
from proj.products.models import Product
from proj.products.forms import ProductForm
from proj.cart.forms import AddToCart

@products.route('/')
def index():
    products_list = Product.query.all()
    return render_template('products/product_list.html', products=products_list)

@products.route('/<int:id>', methods=['GET', 'POST'])
def details(id):
    if 'cart' not in session:
        session['cart'] = []

    product = Product.query.get_or_404(id)

    form = AddToCart(product_id=product.id)
    if form.validate_on_submit():
        # Check if product already in cart
        cart_item = next((item for item in session['cart'] if int(item['id']) == int(product.id)), None)
        
        if cart_item:
            # Update quantity if product already in cart
            cart_item['quantity'] = int(cart_item['quantity']) + int(form.quantity.data)
        else:
            # Add new item to cart
            session['cart'].append({
                'id': int(form.product_id.data),
                'quantity': int(form.quantity.data)
            })
        
        session.modified = True
        return redirect(url_for('products.index'))

    return render_template('products/product_details.html', product=product, form=form)

@products.route('/new', methods=['GET', 'POST'])
@login_required
def create():  # Vulnerability: IDOR and CSRF (check other comments for details)
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            in_stock=form.in_stock.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.index'))
    
    return render_template('products/product_form.html', form=form)

@products.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.in_stock = form.in_stock.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        return redirect(url_for('products.index'))

    return render_template('products/product_form.html', form=form)

@products.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.index'))
