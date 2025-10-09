# Flask Stripe
tutorial: https://7bitramen.medium.com/easy-stripe-subscription-management-in-flask-with-blueprints-5408d50e03a5

# Test Webhooks with the cli
`brew install stripe/stripe-cli/stripe` (OSX)
 - `stripe login`
 - `stripe listen --forward-to localhost:4242/webhook`
 - `stripe trigger payment_intent.succeeded`
 - `python -m flask run --port=4242`
