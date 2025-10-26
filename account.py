import os
import json

from flask import Blueprint, jsonify, request, redirect, current_app, flash
from flask_login import current_user, login_user
from flask_mail import Mail, Message
import logging
from database import query
from dotenv import load_dotenv
import manage
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

account = Blueprint('account', __name__)


@account.route("/test")
def signup():
    """
    TODO send a confirmation link first:

    msg = Message('Twilio SendGrid Test Email', recipients=['mike@centerofwow.com', 'mutinyzoo@gmail.com'])
    msg.body = 'This is a test email!'
    msg.html = '<p>This is a test email!</p>'
    mail.send(msg)
    """
    """ user = manage.create_user(
        request.form['fullname'],
        request.form["email"],
        request.form["password"],
        request.form['orishaname'],
    ) """

    with current_app.app_context():
        mail = Mail()
    # For now just let me know when we have a new registrant
    msg = Message('New New User Registration', recipients=['mike'])
    msg.body = 'New registration for %s.' % "nobody"
    msg.html = '<p>New registration for %s</p>' % 'x@ex.com'
    result = mail.send(msg)
    print(result)
    return json.dumps(msg.body)

@account.route("/register", methods=["POST"])
def create_account_post():
    if request.form["spamtest"] != "pensacola":
        return json.dumps({"error": "This looks like a robot submission. Email help@oghtolal.com for help."})
    if request.form["password"] != request.form["password2"]:
        return json.dumps({"error": "Passwords don't match"})
    info = query("INSERT INTO USERS (username, email, password, hex_key) VALUES (%s, %s, %s, %s) id, hex_key",
                request.form["username"], request.form["email"], request.form["password"], utils.random_hex())
    if isinstance(info[0], str):
        # There's an error.
        return json.dumps({"error": info})
    confirmation_url = request.base_url + "/confirm/%s/%s" % info # yes, that's "/create_account/confirm"

    with current_app.app_context():
        mail = Mail()
    msg = Message('New User Registration', recipients=['mike@mzoo.org'])
    msg.body = """Either you or someone else just created an account at oghtolal.com.

To confirm for %s at %s, please visit %s""" % (request.form["username"], request.form["email"], confirmation_url)
    mail.send(msg)
    return json.dumps({
        "success": "Thanks for registering. Please check your email (%s) for confirmation link... and click it." % request.form["email"]
    })

@account.route("/confirm/<id>/<nonce>")
def confirm_account(id, nonce):
    fullname, user_email = query("UPDATE users SET status=1 WHERE  id=%s AND hex_key=%s RETURNING fullname, email" % (id, nonce))
    if fullname is None:
        flash("Incorrect confirmation link, or link expired. Sorry!")
        return redirect("/account")
    else:
        login_user(manage.User.from_id(id))
        with current_app.app_context():
            mail = Mail()
            adminmsg = Message('New User Registration', recipients=['mike@mzoo.org'])
            adminmsg = "New user %s created with email: %s." % (fullname, user_email)
            studentmsg = Message("Welcome to Osun's Golden Harvest Temple of Love and Light", recipients=[user_email])
            studentmsg = "Hello, %s Your account is confirmed with email %s." % (fullname, user_email)
    flash("Welcome, %s! Your account has been confirmed." % fullname)
    return redirect("/student")
