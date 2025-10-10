# Flask Stripe
tutorial: https://7bitramen.medium.com/easy-stripe-subscription-management-in-flask-with-blueprints-5408d50e03a5
https://flask.palletsprojects.com/en/stable/blueprints/
https://github.com/duplxey/flask-stripe-subscriptions/blob/master/app.py

# Test Webhooks with the cli
`brew install stripe/stripe-cli/stripe` (OSX)
 - `stripe login`
 - `stripe listen --forward-to localhost:4242/payments/webhook`
 - `stripe trigger payment_intent.succeeded`
 - `python -m flask run --port=4242`
