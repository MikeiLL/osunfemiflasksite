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

## Application Scope
### User
- registration
- login
- password reset
- - pwd requirements (perhaps minimum 12 characters)
- status
- classes
- account
- - view
- - edit
- - manage subcriptions
### Public
- view subscription options
- home page view
### Admin
- view users
- edit users
- - set grade level (1-8)
### Mail handling

## Provisioning and Deployment
Heroku, AWS, Linode???

### Products Object
```
{
  "data": [
    {
      "active": true,
      "attributes": [],
      "created": 1759941508,
      "default_price": "price_1SG0NkFObefKa7ZL0LYfX50M",
      "description": "Beginning on your learning journey into Ifa/Orisha",
      "features": [],
      "id": "prod_TCPCXDugSOxuQN",
      "images": [
        "https://files.stripe.com/links/MDB8YWNjdF8xU0VEZFBGT2JlZkthN1pMfGZsX3Rlc3Rfck1WcDZ5N1o0VHNvbjFHU2xmMDluWENt00w4X0G1Mk"
      ],
      "livemode": false,
      "marketing_features": [],
      "metadata": {},
      "name": "Student",
      "object": "product",
      "package_dimensions": null,
      "shippable": null,
      "statement_descriptor": null,
      "tax_code": null,
      "type": "service",
      "unit_label": null,
      "updated": 1759941685,
      "url": null
    }
  ],
  "has_more": false,
  "object": "list",
  "url": "/v1/products"
}
```
### Price Object
```
{
      "active": true,
      "billing_scheme": "per_unit",
      "created": 1759941508,
      "currency": "usd",
      "custom_unit_amount": null,
      "id": "price_1SG0NkFObefKa7ZL0LYfX50M",
      "livemode": false,
      "lookup_key": null,
      "metadata": {},
      "nickname": null,
      "object": "price",
      "product": "prod_TCPCXDugSOxuQN",
      "recurring": {
        "aggregate_usage": null,
        "interval": "month",
        "interval_count": 1,
        "meter": null,
        "trial_period_days": null,
        "usage_type": "licensed"
      },
      "tax_behavior": "unspecified",
      "tiers_mode": null,
      "transform_quantity": null,
      "type": "recurring",
      "unit_amount": 500,
      "unit_amount_decimal": "500"
    }
    ```

### Stripe
Test cards: https://docs.stripe.com/testing#cards

### Product Images helper
`magick -gravity center -background yellow -fill thistle2 -size 100x100 caption:"DG" dedicatedgodchild.png`

stripe.checkout.Session.list(limit=3)
stripe.checkout.Session.retrieve("cs_test_a1ouFxH26VhCOtlEkrKgml9aUJj4Id7n44CbYsYXOcBtS3g49tub2JZDGj")
stripe.checkout.Session.list_line_items("cs_test_a1ouFxH26VhCOtlEkrKgml9aUJj4Id7n44CbYsYXOcBtS3g49tub2JZDGj")
ses = stripe.checkout.Session.list(customer="cus_TD9FBhMjlQipgp")
ses.data[0].id
