from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def entry_point():
    return render_template('index.html')
    # return 'Hello World!'

@app.route('/about')
def about():
    return 'this is about page'

if __name__ == '__main__':
    app.run(debug=True, port=8000)