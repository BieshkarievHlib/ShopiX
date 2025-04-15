from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, logout_user, login_required, current_user

from proj import app, db
from proj.models import User, Product, Order, OrderToProduct
from proj.forms import ProductForm, UserForm, LoginForm, OrderForm, AddToCart

# Template helper function to get product by ID
@app.context_processor
def utility_processor():
    def get_product(product_id):
        return Product.query.get(int(product_id))
    return {'get_product': get_product}

@app.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/products/<int:id>',methods=['GET','POST'])
def product_details(id):
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
        flash('Товар додано до кошика!', 'success')
        return redirect(url_for('product_list'))

    return render_template('product_details.html', product=product, form=form)

@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def product_create():                               #Vulnerability: IDOR and CSRF (check other comments for details)
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
        return redirect(url_for('product_list'))
    
    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/edit', methods=['GET','POST'])
@login_required
def product_edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name=form.name.data
        product.in_stock=form.in_stock.data
        product.description=form.description.data
        product.price=form.price.data
        db.session.commit()
        return redirect(url_for('product_list'))

    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def product_delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))

@app.route('/cart', methods=['GET'])
def cart():
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
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/update/<int:id>', methods=['POST'])
def update_cart(id):
    if 'cart' not in session or id >= len(session['cart']):
        return redirect(url_for('cart'))
    
    quantity = int(request.form.get('quantity', 1))
    if quantity > 0:
        session['cart'][id]['quantity'] = quantity
        session.modified = True
        flash('Кількість товару оновлено!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:id>')
def remove_from_cart(id):
    if 'cart' in session and id < len(session['cart']):
        session['cart'].pop(id)
        session.modified = True
        flash('Товар видалено з кошика!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/cart/clear')
def clear_cart():
    session['cart'] = []
    session.modified = True
    flash('Кошик очищено!', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or len(session['cart']) == 0:
        flash('Ваш кошик порожній!', 'warning')
        return redirect(url_for('product_list'))
    
    form = OrderForm()
    
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            delivery=form.delivery.data
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
            else:
                flash(f'Товар "{product.name}" недоступний у вказаній кількості!', 'danger')
                return redirect(url_for('cart'))
        
        db.session.commit()
        session['cart'] = []
        session.modified = True
        
        flash('Замовлення успішно оформлено!', 'success')
        return redirect(url_for('product_list'))
        
    return render_template('checkout.html', form=form, cart=session['cart'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product_list'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('product_list'))
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('product_list'))

@app.route('/user/new', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('product_list'))
        
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('user_details', id=user.id))
    
    return render_template('user_form.html', form=form)

@app.route('/user/<int:id>')
@login_required
def user_details(id):
    user = User.query.get_or_404(id)
    return render_template('user_details.html', user=user)

@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(id):
        # VULNERABILITY: Indirect object reference can provide unauthorized access.
        # - Access to the page does not require any rights or privileges
        # - No access management
        # - Vulnerable to domain enumerating and IDOR
        # - Should use access control
    user = User.query.get(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('user_details', id=user.id))

    return render_template('user_form.html', form=form)