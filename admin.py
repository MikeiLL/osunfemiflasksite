from flask import Blueprint, jsonify, request, render_template, redirect, flash
from flask_login import LoginManager, current_user, login_user
import stripe
import os
import logging
import psycopg2
from dotenv import load_dotenv
import manage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

_conn = psycopg2.connect(DATABASE_URL)

admin = Blueprint('admin', __name__)
# This allows us to easily manage Stripe related env vairables
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "webhook_secret": os.environ["STRIPE_WEBHOOK_SECRET"]
}
domain_url = os.environ["DOMAIN_URL"]
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: <https://dashboard.stripe.com/apikeys>
stripe.api_key = stripe_keys["secret_key"]

# TODO look into https://docs.stripe.com/api/customer_portal/sessions

@admin.route("/")
def index():
    if not (current_user and hasattr(current_user, 'user_level') and current_user.user_level > 1):
        return redirect("/")
    return "hi, admin go to slash library for something to do"

@admin.route("/library")
def library():
    if not (current_user and hasattr(current_user, 'user_level') and current_user.user_level > 1):
        return redirect("/")

    with _conn, _conn.cursor() as cur:
        cur.execute("SELECT title, description, filename, minimum_grade, active FROM library_content")
        library_content = cur.fetchall()
        print(library_content)
    return render_template("library_admin.html", user=current_user, library_content=library_content)


# see https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
@admin.route("/library", methods=["POST"])
def new_library_document():
    # check if the post request has the file part
    if 'document' not in request.files:
        flash('No file part')
        return redirect(request.url, 303)
    doc = request.files['document']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if doc.filename == '':
        flash('No selected file')
        return redirect(request.url, 303)
    with _conn, _conn.cursor() as cur:
        cur.execute("""
            INSERT INTO library_content
                (title, description, filename, filecontent, active, minimum_grade)
            VALUES (%s, %s, %s, %s, true, %s) returning id
        """, (
            request.form["title"],
            request.form["description"],
            doc.filename,
            doc.read(),
            request.form["minimum_grade"],
        ))
        id = cur.fetchone()[0]
    flash('Succesfully uploaded %s' % request.form["title"])
    return redirect(request.url, 303)
