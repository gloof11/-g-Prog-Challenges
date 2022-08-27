# Stores the static routes for auth #
#####################################
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# define the name of the blueprint
auth = Blueprint('auth', __name__)
 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confPass = request.form.get('confPass')

        # check if user is valid
        user = User.query.filter_by(username=username).first()
        if user:
            #check if password is valid
            if check_password_hash(user.password, password):
                flash("Login Success!", category='success')

                # Store user session
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", category='error')
        else:
            flash("User does not exist", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # logout the user
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confPass = request.form.get('confPass')

        # check if user is exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists", category='error')
        elif len(username) < 4:
            flash("Username must be greater than 4 chars", category='error')
        elif password != confPass:
            flash("Passwords don't match", category='error')
        elif len(password) < 7:
            flash("Password must be greater than 7 chars", category='error')
        else:
            # define the new user
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            
            # add user to the database
            db.session.add(new_user)
            db.session.commit()

            # Store user session
            login_user(user, remember=True)

            flash("Account created!", category='success')

            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)