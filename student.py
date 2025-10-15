from flask import Blueprint, jsonify, request, render_template, redirect, make_response
from flask_login import LoginManager, current_user, login_user
import stripe
import os
import logging
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from database import query, dict_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

student = Blueprint('student', __name__)

@student.before_request
def restrict_bp_to_students():
    if not (current_user and hasattr(current_user, 'user_level') and current_user.user_level >= 1):
        return redirect("/")

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

@student.route("/")
def library():
    #stripecustomer = stripe.Customer.retrieve(current_user.stripe_customer_id)
    MAX_GRADE = 6
    user_grade = current_user.grade_level
    if user_grade < MAX_GRADE:
        subscriptions = stripe.Subscription.list(customer=current_user.stripe_customer_id, status="active")
        if (len(subscriptions.data) >= 1): user_grade = MAX_GRADE
    mylibrary = dict_query("""
        SELECT * FROM library_content
        WHERE active = true AND minimum_grade <= %s
    """, (user_grade,))
    return render_template("student.html", user=current_user, mylibrary=mylibrary)

@student.route('/docs/<id>')
def get_pdf(id):
        subscriptions = stripe.Subscription.list(customer=current_user.stripe_customer_id, status="active")
        if not subscriptions.data:
            return render_template("400_generic.html", user=current_user, e="Whoops. This requires a subscription."), 403
        binary_pdf = query("SELECT filecontent FROM library_content WHERE id = %s", (id,))[0]
        if binary_pdf:
            response = make_response(bytes(binary_pdf[0]))
            response.headers['Content-Type'] = 'application/pdf'
            #response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename' (for download)
        else:
            return render_template("400_generic.html", user=current_user, e="Whoops the file you were looking for doesn't seem to exist."), 404
        return response
