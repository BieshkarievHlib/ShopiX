from flask import render_template, redirect, url_for, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, identity_changed, AnonymousIdentity

from proj import db
from proj.auth import auth
from proj.auth.models import User, Role
from proj.auth.forms import LoginForm, UserForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page or url_for('products.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            identity_changed.send(current_app._get_current_object(),
                                 identity=Identity(user.id))
            return redirect(next_page or url_for('products.index'))
        
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    
    identity_changed.send(current_app._get_current_object(),
                         identity=AnonymousIdentity())
    
    return redirect(url_for('products.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))
        
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role_id=Role.query.filter_by(name='user').first().id
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                             identity=Identity(user.id))
        
        return redirect(url_for('auth.profile', id=user.id))
    
    return render_template('auth/user_form.html', form=form)

@auth.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('auth/user_details.html', user=user)

@auth.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get(id)
    if user.id != current_user.id:
        return redirect(url_for('auth.edit_profile', id=current_user.id))

    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('auth.profile', id=user.id))

    return render_template('auth/user_form.html', form=form)
