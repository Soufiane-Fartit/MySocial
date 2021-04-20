from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email==email).first()
        if not user :
            flash('User with that email does not exist. Please register first.')
        elif check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.Index'))
        else :
            flash('Wrong password. Try again.')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password = generate_password_hash(password, method='sha256')
        user = User.query.filter(User.email==email).first()
        if user :
            flash('User Already exists')
        else :
            new_user = User(first_name, last_name, email, password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created')
    return render_template('auth/register.html')