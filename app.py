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
from datetime import datetime

from flask import Flask, jsonify, request, render_template, redirect, flash
""" url_for, Response, send_from_directory,  """
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
import manage
import psycopg2
from dotenv import load_dotenv

load_dotenv()
from payment import payment
from student import student
from admin import admin
from images import images

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USE_TLS'] = os.environ['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)


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
app.register_blueprint(images, url_prefix="/images")

@app.context_processor
def inject_date():
    return dict(year=datetime.now().year)

@app.route("/")
def index():
    items = [p for p in stripe.Product.list() if p['active']]
    prices = {p["product"]: p for p in stripe.Price.list()}
    # mutate the product to add the price
    for p in items:
         p["price"] = prices.get(p["id"])
    subscriptions = [item for item in items if item.price.recurring]
    purchases = [item for item in items if not item.price.recurring]
    return render_template("index.html", subscriptions=subscriptions, purchases=purchases, user=current_user)


@app.route("/login")
def login_get():
    return render_template("login.html", user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    """
    TODO send a confirmation link first:

    msg = Message('Twilio SendGrid Test Email', recipients=['mike@centerofwow.com', 'mutinyzoo@gmail.com'])
    msg.body = 'This is a test email!'
    msg.html = '<p>This is a test email!</p>'
    mail.send(msg)
    """
    user = manage.create_user(
        request.form['fullname'],
        request.form["email"],
        request.form["password"],
        request.form['orishaname'],
    )
    # For now just let me know when we have a new registrant
    msg = Message('New User Registration', recipients=['mike@mzoo.org', 'mutinyzoo@gmail.com'])
    msg.body = 'New registration for %s.' % request.form["email"]
    msg.html = '<p>New registration for %s</p>' % request.form["email"]
    mail.send(msg)
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

@app.route("/cancel")
def cancel():
    flash('Purchase not completed.')
    return redirect("/")

if __name__ == "__main__":
    # # If we're running with gunicorn, we need to start the websocket server
    # # So swap comment on following block with the next one
    import logging
    logging.basicConfig(level=logging.INFO)
    if "PORT" not in os.environ: os.environ["PORT"] = "4242"

    app.run(debug=True, port=4242)
