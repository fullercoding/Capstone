from . import bp as auth
from flask import render_template, request, flash, redirect, url_for
from app.models import User
from flask_login import login_user,login_required,logout_user, current_user
from .forms import LoginForm, RegisterForm, EditProfileForm
from config import Config

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # LOGIN THE USER HERE
        email = form.email.data.lower()
        password = form.password.data
                                #colname = value from form
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            #Login Success
            flash("Successfully logged in", 'success')
            login_user(u)
            return redirect(url_for('main.homepage'))
        
        error_string = "Incorrect Email/Password Combo"
        return render_template('login.html.j2', loginerror=error_string, form=form)
    return render_template('login.html.j2', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))




@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name":  form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data
        }

        #Create empty user object to become our new user
        new_user_object = User()

        #build the user from the form data
        new_user_object.from_dict(new_user_data)

        #save new user to the database
        new_user_object.save()

        #flash user telling them they registered
        flash("Successfully registered", "success")
        return redirect(url_for("auth.login"))

    return render_template('register.html.j2', form=form)

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        edited_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name":  form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data
        }
        user = User.query.filter_by(email = edited_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash('Email is already in use','danger')
            return redirect('/edit_profile')
        current_user.from_dict(edited_user_data)
        current_user.save()
        flash("Profile Updated", 'success')
        return redirect(url_for("main.homepage"))



    return render_template('register.html.j2', form= form)