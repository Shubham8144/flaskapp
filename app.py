from config import app
from flask import redirect, render_template, url_for
from forms import LoginForm, RegistrationForm


@app.route("/")
def entry_point():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (
            form.email.data == "admin@bestpeers.com"
            and form.password.data == "password"
        ):
            return redirect(url_for("/"))
        else:
            return "not validated"
    return render_template("login.html", title="Login", form=form)


@app.route("/about")
def about():
    return "this is about page"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
