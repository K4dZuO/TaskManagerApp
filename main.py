from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/test')
def get_test_page():
    return render_template("ordinary.html")

if __name__ == "__main__":
    app.run(debug=True)

