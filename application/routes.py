from datetime import datetime, timedelta
from .models import User, Widget
from flask import flash, jsonify, redirect, render_template, url_for, request
from application import app, db , bcrypt
from .forms import LoginForm, RegistrationForm, WidgetForm
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import exc
import jwt
from functools import wraps
from flask_login import current_user, login_required, login_user, logout_user


def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated



@app.route("/")
@token_required
def entry_point():
    return render_template("index.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect (url_for("entry_point"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect (url_for("entry_point"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)            
            flash("You have been logged in!", "success")
            token = jwt.encode({
                'user': form.email.data,
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
            }, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('utf-8')})
            # return redirect(url_for("entry_point"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/verify/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)

@app.route("/about")
def about():
    return "this is about page"

@login_required
@app.route("/widget")
def widget():
    widgets = Widget.query.all()
    return render_template("widget.html", widgets=widgets)

@login_required
@app.route("/createwidget", methods=['GET', 'POST'])
def create_widget():
    widget_list = Widget.query.all()
    form = WidgetForm()
    if form.validate_on_submit:
        new_widget = Widget(name=form.name.data)
        db.session.add(new_widget)
        try:
            db.session.commit()
            flash('Widget has been created!', 'success') 
            return redirect(url_for('create_widget'))
        except exc.IntegrityError:
            db.session.rollback()
    return render_template('create_widget.html', title='Create Widget',
                           form=form, widget_list=widget_list)


@app.route("/widget/<int:widget_id>/delete", methods=['POST'])
@login_required
def delete_widget(widget_id):
    del_widget = Widget.query.get_or_404(widget_id)
    db.session.delete(del_widget)
    db.session.commit()
    flash('Your widget has been deleted!', 'success')
    return redirect(url_for('create_widget'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/widget/<int:widget_id>/update", methods=['GET', 'POST'])
@login_required
def update_widget(widget_id):
    widget = Widget.query.get_or_404(widget_id)
    print(widget.name)
    form = WidgetForm()
    if form.validate_on_submit():
        widget.name = form.name.data
        db.session.commit()
        flash('Your widget has been updated!', 'success')
        return redirect(url_for('create_widget'))
    elif request.method == 'GET':
        form.name.data = widget.name
    return redirect(url_for('create_widget'))