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
    product = Product.query.get(id)
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
    product = Product.query.get(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name=form.name.data,
        product.in_stock=form.in_stock.data
        db.session.add(product)
        db.session.commit()
        flash('Продукт успішно відредаговано!', 'success')
        return redirect(url_for('product_list'))
    else:
        flash('Щось неправильно... Спробуйте знову!', 'fail')

    return render_template('product_form.html', form=form)

@app.route('/products/<int:id>/delete', methods=['POST'])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Продукт видалено!', 'success')

    return redirect(url_for('product_list'))