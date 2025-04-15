from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from proj import app, db
from proj.models import User, Product, ProductType
from proj.forms import ProductForm, UserForm, LoginForm

@app.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/products/<int:id>')
def product_details(id):
    product = Product.query.get(id)
    return render_template('product_details.html', product=product)

@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            in_stock=form.in_stock.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_list'))
    
    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/edit', methods=['GET','POST'])
@login_required
def product_edit(id):
    product = Product.query.get(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name=form.name.data
        product.in_stock=form.in_stock.data
        product.description=form.description.data
        db.session.commit()
        return redirect(url_for('product_list'))

    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))

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
    user = User.query.get(id)
    return render_template('user_details.html', user=user)

@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(id):
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

