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
from payment import payment
import admin
from dotenv import load_dotenv
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

load_dotenv()



# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return admin.User.from_id(int(id))

app.register_blueprint(payment, url_prefix="/payment")

@app.route("/")
def index():
    products = stripe.Product.list()
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
    data = request.form
    print(data)
    return jsonify({'hello': "world"})
    user = admin.create_user()
    return jsonify({'hello': "world"})

@app.route("/login", methods=["POST"])
def login_post():
    user = admin.User.from_credentials(
        request.form["email"],
        request.form["password"]
    )
    if user:
        login_user(user)
        return redirect('/')
    else:
        flash("Invalid email or password")
        return redirect("/")

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
