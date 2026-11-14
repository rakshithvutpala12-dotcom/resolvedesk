from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from .extensions import db
from .models import User
from .forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.active and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Welcome back.', 'success')
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'warning')
        else:
            user = User(name=form.name.data.strip(), email=email, department=form.department.data.strip() or 'General', role='employee')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created. You can now sign in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))
