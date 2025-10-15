from flask import Blueprint, jsonify, request
from flask_login import LoginManager, current_user, login_user
import stripe
import os
import logging
from database import query
from dotenv import load_dotenv
import manage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

payment = Blueprint('payment', __name__)
# This allows us to easily manage Stripe related env vairables
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "webhook_secret": os.environ["STRIPE_WEBHOOK_SECRET"]
}
domain_url = os.environ["DOMAIN_URL"]
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: <https://dashboard.stripe.com/apikeys>
stripe.api_key = stripe_keys["secret_key"]

def increase_grade_level(amt):
    query("update users set grade_level = %s where id = %s", (amt, current_user.id))
    return True

@payment.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.json
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer=current_user.stripe_customer_id,
        mode="subscription" if data["recurring"] == 'true' else "payment",
        line_items=[{"price": data["price_id"], "quantity": 1}],
        success_url=f"{domain_url}/student?student_id={current_user.id}",
        cancel_url=f"{domain_url}/cancel",
    )
    max_grade_level = query("select max(level) from grade_levels")[0][0]
    if not current_user.grade_level == max_grade_level:
        list_line_items = stripe.checkout.Session.list_line_items(checkout_session.id)
        product = stripe.Product.retrieve(list_line_items.data[0].price.product)
        # TODO increase grade_level of subscriptions also, but with webhook prolly
        if product.metadata.grade_increase:
            increase_grade_level(min(current_user.grade_level + int(product.metadata.grade_increase), max_grade_level))
    return jsonify({"url": checkout_session.url})

@payment.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["webhook_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400
    """     from datetime import datetime
    with open("event_data_objects", "a") as f:
        print(datetime.now(), file=f)
        print('', file=f)
        print(event['type'], file=f)
        print(event['data'], file=f) """
  # There are alot of event types you can listen for and I have listed all of them below
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        logger.info("Payment succeeded")
        session = event['data']['object']
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
    elif event['type'] == 'customer.created':
        customer = event['data']['object']
    elif event['type'] == 'customer.deleted':
        customer = event['data']['object']
    elif event['type'] == 'customer.updated':
        customer = event['data']['object']
    elif event['type'] == 'customer.discount.created':
        discount = event['data']['object']
    elif event['type'] == 'customer.discount.deleted':
        discount = event['data']['object']
    elif event['type'] == 'customer.discount.updated':
        discount = event['data']['object']
    elif event['type'] == 'customer.source.created':
        source = event['data']['object']
    elif event['type'] == 'customer.source.deleted':
        source = event['data']['object']
    elif event['type'] == 'customer.source.expiring':
        source = event['data']['object']
    elif event['type'] == 'customer.source.updated':
        source = event['data']['object']
    elif event['type'] == 'customer.subscription.created':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.deleted':
        subscription_oject = event["data"]["object"]
        handle_canceled_subscription(subscription_oject)
    elif event['type'] == 'customer.subscription.paused':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.pending_update_applied':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.pending_update_expired':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.resumed':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.trial_will_end':
        subscription_object = event['data']['object']
    elif event['type'] == 'customer.subscription.updated':
        subscription_oject = event["data"]["object"]
        handle_update_subscription(subscription_oject)
    elif event['type'] == 'customer.tax_id.created':
      tax_id = event['data']['object']
    elif event['type'] == 'customer.tax_id.deleted':
      tax_id = event['data']['object']
    elif event['type'] == 'customer.tax_id.updated':
      tax_id = event['data']['object']

    return "Success", 200

def handle_canceled_subscription(subscription_oject):
  print(subscription_oject)

def handle_update_subscription(subscription_oject):
  print(subscription_oject)

def handle_checkout_session(session):
  print(session)

stripe.billing_portal.Configuration.create(
    business_profile={"headline": "Your Business Name"},
    features={
        "invoice_history": {"enabled": True},
        "customer_update": {"enabled": True, "allowed_updates": ["address", "name"]},
        # Add other features as needed
    },
    default_return_url="http://127.0.0.1:4242/",
)
