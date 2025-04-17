from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Назва продукту', validators=[DataRequired(message='Назва не може бути пустою!'), Length(max=64)])
    in_stock = IntegerField('Кількість на складі',validators=[NumberRange(min=0, message='Кількість не може бути менше нуля!')])
    description = TextAreaField('Опис продукту', validators=[DataRequired()])
    price = FloatField('Ціна продукту', validators=[NumberRange(min=0.0, message='Ціна не може бути менше нуля!')])
    submit = SubmitField('Створити продукт')

    class Meta:
        csrf = False
        # VULNERABILITY: CSRF Protection Disabled
        # - Form has no CSRF protection
        # - Vulnerable to Cross-Site Request Forgery attacks
        # - Attackers can submit forms on behalf of authenticated users
        # - Should enable CSRF protection for all forms
