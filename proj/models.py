# Import models from blueprints for backwards compatibility
from proj.auth.models import User
from proj.products.models import Product, ProductType
from proj.cart.models import Order, OrderToProduct 