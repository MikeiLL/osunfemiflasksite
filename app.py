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

from flask import Flask, jsonify, request, render_template
from payment import payment
from dotenv import load_dotenv

load_dotenv()
# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

app = Flask(__name__)
app.register_blueprint(payment, url_prefix="/payment")
""" @app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True) """

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
