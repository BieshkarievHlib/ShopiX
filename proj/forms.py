from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, PasswordField, EmailField, BooleanField, FloatField, SelectField, HiddenField, FieldList, FormField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Regexp, Email, ValidationError
from proj.models import User, Product

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

class UserForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired(),Length(max=64)])
    surname = StringField('Прізвище', validators=[DataRequired(),Length(max=64)])

    username = StringField('Логін', validators=[DataRequired('Логін мати обов\'язково!'),Length(max=32)])
    password = PasswordField('Пароль', validators=[
    DataRequired('Пароль мати обов\'язково!'),
    Length(min=8, message='Пароль має складатися щонайменше з 8 символів.'),
    Regexp(
        regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
        message='Пароль має містити щонайменше одну цифру та одну літеру.'
    ),
    EqualTo('confirm', message='Паролі не співпдаають. Спробуйте знову!')
    ])

    confirm = PasswordField('Підтвердіть пароль', validators=[DataRequired('Необхідно підтвердити пароль')])
    email = EmailField('E-mail', validators=[
        DataRequired(message='Необхідно ввести електронну пошту.'),
        Email(message='Невірна адреса. Спробуйте знову!')
    ])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я користувача вже зайняте. Будь ласка, виберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ця електронна адреса вже зареєстрована.')

class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')
    
    # VULNERABILITY: Login Form Security Issues
    # - No rate limiting on login attempts
    # - No account lockout after failed attempts
    # - No CAPTCHA or other bot protection
    # - Generic error messages (don't reveal if username exists)
    # - Should implement proper login security measures