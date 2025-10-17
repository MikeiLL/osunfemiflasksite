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

### Image Magick Thumbnail Classes
magick ../Ifa\ Classes/Sept2025/PDF\ Files/Class8.pdf[0] class_eight_thumbnail.png

### Heroku
`heroku addons --help`
`heroku addons services`
`heroku addons:add heroku-postgresql`
`heroku addons:info postgresql-metric-86056`
`heroku addons:add heroku-postgresq`
`heroku addons:docs heroku-postgresql`
`heroku pg:psq`
`heroku config`, `heroku config:set`

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

sessions = stripe.checkout.Session.list(customer="cus_TD9FBhMjlQipgp")
sessions.data[0].id
lineitems = stripe.checkout.Session.list_line_items("cs_test_a1ouFxH26VhCOtlEkrKgml9aUJj4Id7n44CbYsYXOcBtS3g49tub2JZDGj")
lineitems.data[0].price.product
stripe.Product.retrieve('prod_TDFkCHVTwleM61')
stripe.Subscription.list(customer="cus_TD9FBhMjlQipgp", status="all")

### This is a customers subscription object:
```
{
      "application": null,
      "application_fee_percent": null,
      "automatic_tax": {
        "disabled_reason": null,
        "enabled": false,
        "liability": null
      },
      "billing_cycle_anchor": 1760319343,
      "billing_cycle_anchor_config": null,
      "billing_mode": {
        "flexible": null,
        "type": "classic"
      },
      "billing_thresholds": null,
      "cancel_at": null,
      "cancel_at_period_end": false,
      "canceled_at": null,
      "cancellation_details": {
        "comment": null,
        "feedback": null,
        "reason": null
      },
      "collection_method": "charge_automatically",
      "created": 1760319343,
      "currency": "usd",
      "current_period_end": 1762997743,
      "current_period_start": 1760319343,
      "customer": "cus_TD9FBhMjlQipgp",
      "days_until_due": null,
      "default_payment_method": "pm_1SHafrFObefKa7ZLibp9AYVW",
      "default_source": null,
      "default_tax_rates": [],
      "description": null,
      "discount": null,
      "discounts": [],
      "ended_at": null,
      "id": "sub_1SHafrFObefKa7ZLls2SYg9k",
      "invoice_settings": {
        "account_tax_ids": null,
        "issuer": {
          "type": "self"
        }
      },
      "items": {
        "data": [
          {
            "billing_thresholds": null,
            "created": 1760319344,
            "current_period_end": 1762997743,
            "current_period_start": 1760319343,
            "discounts": [],
            "id": "si_TE2lBAr5UOr2FQ",
            "metadata": {},
            "object": "subscription_item",
            "plan": {
              "active": true,
              "aggregate_usage": null,
              "amount": 500,
              "amount_decimal": "500",
              "billing_scheme": "per_unit",
              "created": 1759941508,
              "currency": "usd",
              "id": "price_1SG0NkFObefKa7ZL0LYfX50M",
              "interval": "month",
              "interval_count": 1,
              "livemode": false,
              "metadata": {},
              "meter": null,
              "nickname": null,
              "object": "plan",
              "product": "prod_TCPCXDugSOxuQN",
              "tiers_mode": null,
              "transform_usage": null,
              "trial_period_days": null,
              "usage_type": "licensed"
            },
            "price": {
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
            },
            "quantity": 1,
            "subscription": "sub_1SHafrFObefKa7ZLls2SYg9k",
            "tax_rates": []
          }
        ],
        "has_more": false,
        "object": "list",
        "total_count": 1,
        "url": "/v1/subscription_items?subscription=sub_1SHafrFObefKa7ZLls2SYg9k"
      },
      "latest_invoice": "in_1SHafrFObefKa7ZLGyV2jKn7",
      "livemode": false,
      "metadata": {},
      "next_pending_invoice_item_invoice": null,
      "object": "subscription",
      "on_behalf_of": null,
      "pause_collection": null,
      "payment_settings": {
        "payment_method_options": {
          "acss_debit": null,
          "bancontact": null,
          "card": {
            "network": null,
            "request_three_d_secure": "automatic"
          },
          "customer_balance": null,
          "konbini": null,
          "sepa_debit": null,
          "us_bank_account": null
        },
        "payment_method_types": [
          "card"
        ],
        "save_default_payment_method": "off"
      },
      "pending_invoice_item_interval": null,
      "pending_setup_intent": null,
      "pending_update": null,
      "plan": {
        "active": true,
        "aggregate_usage": null,
        "amount": 500,
        "amount_decimal": "500",
        "billing_scheme": "per_unit",
        "created": 1759941508,
        "currency": "usd",
        "id": "price_1SG0NkFObefKa7ZL0LYfX50M",
        "interval": "month",
        "interval_count": 1,
        "livemode": false,
        "metadata": {},
        "meter": null,
        "nickname": null,
        "object": "plan",
        "product": "prod_TCPCXDugSOxuQN",
        "tiers_mode": null,
        "transform_usage": null,
        "trial_period_days": null,
        "usage_type": "licensed"
      },
      "quantity": 1,
      "schedule": null,
      "start_date": 1760319343,
      "status": "active",
      "test_clock": null,
      "transfer_data": null,
      "trial_end": null,
      "trial_settings": {
        "end_behavior": {
          "missing_payment_method": "create_invoice"
        }
      },
      "trial_start": null
    }
    ```

- student document access by grade
- for now ignore concept of purchasing grades
- admin library screen
- basic css
