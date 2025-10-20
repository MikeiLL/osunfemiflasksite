from flask import Blueprint, jsonify, request, render_template, redirect, make_response
from flask_login import LoginManager, current_user, login_user
import stripe
import os
import logging
import psycopg2
import psycopg2.extras
import time
from datetime import date, datetime
import locale
from dotenv import load_dotenv
from database import query, dict_query

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

student = Blueprint('student', __name__)

@student.context_processor
def inject_date():
    return dict(year=datetime.now().year)

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

@student.route("/cancel", methods=["post"])
def cancel_subscription():
    data = request.json()
    subscription_id = data['subscription_id']
    cancellation = stripe.Subscription.cancel(subscription_id)
    return jsonify({"message": "subscription cancelled"})

@student.route("/")
def library():
    #stripecustomer = stripe.Customer.retrieve(current_user.stripe_customer_id)
    MAX_GRADE = 6
    user_grade = current_user.grade_level
    subscriptions = stripe.Subscription.list(customer=current_user.stripe_customer_id, status="all")
    # other options are cancelled,
    # ended (subscriptions that are canceled and subscriptions that are expired due to incomplete payment)
    # and all.
    student_subscriptions = []
    for sub in subscriptions.data:
        product = stripe.Product.retrieve(sub.plan.product)
        student_subscriptions.append({
            "id": sub.id,
            "created": datetime.fromtimestamp(sub.created).strftime('%d %b, %Y'),
            #"current_period_start": date.fromtimestamp(sub.current_period_start).strftime('%d %b, %Y'),
            "current_period_end": date.fromtimestamp(sub.current_period_end).strftime('%d %b, %Y'),
            "status": "active" if sub.plan.active else "expired",
            "amount": locale.currency(sub.plan.amount / 100),
            "interval": sub.plan.interval,
            "interval_count": sub.plan.interval_count,
            "product_name": product.name,
        })
    print(student_subscriptions[0])
    if user_grade < MAX_GRADE:
        if (len(subscriptions.data) >= 1): user_grade = MAX_GRADE
    mylibrary = dict_query("""
        SELECT * FROM library_content
        WHERE active = true AND minimum_grade <= %s
        ORDER BY filename
    """, (user_grade,))
    return render_template("student.html", user=current_user, mylibrary=mylibrary, student_subscriptions=student_subscriptions)

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
