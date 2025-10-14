# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python app.py
#   or to run on a different port python3 -m flask run --port=some thing

import json
import os
import stripe

from flask import Flask, jsonify, request, render_template, redirect, flash
""" url_for, Response, send_from_directory,  """
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from payment import payment
from student import student
from admin import admin
import manage
import psycopg2
from dotenv import load_dotenv
import time

load_dotenv()

_conn = psycopg2.connect(os.environ["DATABASE_URL"])

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


def cache_bust(filename):
    stat = os.stat('static/' + filename)
    return f"{filename}?mtime={stat.st_mtime}"

app.jinja_env.globals.update(cache_bust=cache_bust)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return manage.User.from_id(int(id))

app.register_blueprint(payment, url_prefix="/payment")
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(admin, url_prefix="/admin")

@app.route("/")
def index():
    products = [p for p in stripe.Product.list() if p['active']]
    prices = {p["product"]: p for p in stripe.Price.list()}
    # mutate the product to add the price
    for p in products:
         p["price"] = prices.get(p["id"])
    return render_template("index.html", products=products, user=current_user)


@app.route("/login")
def login_get():
    return render_template("login.html", user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    user = manage.create_user(
        request.form['fullname'],
        request.form["email"],
        request.form["password"],
        request.form['orishaname'],
    )
    return json.dumps(user)

@app.route("/login", methods=["POST"])
def login_post():
    user = manage.User.from_credentials(
        request.form["email"],
        request.form["password"]
    )
    if user:
        login_user(user)
        return jsonify(user)
    else:
        return jsonify({'error': "Invalid email or password"})

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    # # If we're running with gunicorn, we need to start the websocket server
    # # So swap comment on following block with the next one
    import logging
    logging.basicConfig(level=logging.INFO)
    if "PORT" not in os.environ: os.environ["PORT"] = "4242"

    app.run(debug=True, port=4242)
