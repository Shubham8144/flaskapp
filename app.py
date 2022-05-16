from flask import render_template, url_for, redirect, flash
from forms import LoginForm, RegistrationForm

from config import app


@app.route("/")
def entry_point():
    return render_template("index.html", title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@d.com' and form.password.data == '123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('entry_point'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/about")
def about():
    return "this is about page"


if __name__ == "__main__":
    app.run(debug=True)
