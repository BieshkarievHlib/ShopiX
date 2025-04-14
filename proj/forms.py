from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Назва продукту', validators=[DataRequired(), Length(max=64)])
    in_stock = IntegerField('Кількість на складі',validators=[NumberRange(min=0)])
    submit = SubmitField('Створити продукт')

    class Meta:
        csrf = False    #Спеціально додаємо вразливість
    