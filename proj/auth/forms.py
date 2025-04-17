from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Email, ValidationError

from proj.auth.models import User

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
    
    submit = SubmitField('Зареєструватися')

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
