import os
from dotenv import load_dotenv
import stripe

load_dotenv()

"""Generate Invoice for User Orders"""


def strip_payment_gateway(total_amount, email):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    invoice = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'cart',
                        },
                        'unit_amount': int(total_amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=os.environ.get('HOST')+'/templates/success.html',
                cancel_url=os.environ.get('HOST')+'/templates/cancel.html',
            )
    card_obj = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 7,
            "exp_year": 2023,
            "cvc": "123",
        },
    )
    customer = stripe.Customer.create(
        email=email, payment_method=card_obj.id
    )
    stripe.PaymentIntent.create(
        customer=customer.id,
        payment_method=card_obj.id,
        currency="inr",
        amount=int(total_amount * 100),
    )
    return invoice
