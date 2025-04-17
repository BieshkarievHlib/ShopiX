from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class AddToCart(FlaskForm):
    product_id = HiddenField('ID', validators=[DataRequired()])
    quantity = IntegerField('Кількість', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Додати до кошику')

class OrderForm(FlaskForm):
    delivery = SelectField('Оберіть спосіб доставки',
                          validators=[DataRequired(message='Необхідно обрати спосіб доставки!')],
                          choices=[('nova_poshta', 'Нова пошта'), ('ukrposhta', 'Укрпошта'), ('self_pickup', 'Самовивіз')], 
                          default='self_pickup')
    submit = SubmitField('Оформити замовлення')
    
    # VULNERABILITY: No Validation of Delivery Address
    # - No required validation for address when delivery is selected
    # - No verification of address format or existence
    # - Could lead to failed deliveries or attacks via specially crafted addresses
