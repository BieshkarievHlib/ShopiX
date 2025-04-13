from flask import render_template

from proj import app
from proj.models import User, Product, ProductType

@app.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@app.route('/products/<int:id>')
def product_details(id):
    product = Product.query.all(id=id)
    return render_template('product_details.html', product=product)

