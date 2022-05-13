from flask import render_template

from config import app


@app.route("/")
def entry_point():
    return render_template("index.html")


@app.route("/about")
def about():
    return "this is about page"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
