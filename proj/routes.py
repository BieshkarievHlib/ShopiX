from flask import render_template, flash, redirect, url_for

from proj import app, db
from proj.models import User, Product, ProductType
from proj.forms import ProductForm

@app.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/products/<int:id>')
def product_details(id):
    product = Product.query.all(id=id)
    return render_template('product_details.html', product=product)

@app.route('/products/new', methods=['GET', 'POST'])
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            in_stock=form.in_stock.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Продукт успішно додано!', 'success')
        return redirect(url_for('product_list'))
    else:
        flash('Щось неправильно... Спробуйте знову!', 'fail')
    
    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/edit', methods=['GET','POST'])
def product_edit(id):
    form = ProductForm(obj=Product.query(id=id))
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            in_stock=form.in_stock.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Продукт успішно додано!', 'success')
        return redirect(url_for('product_list'))
    else:
        flash('Щось неправильно... Спробуйте знову!', 'fail')
    
    return render_template('product_form.html', form=form)