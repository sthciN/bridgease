from db.database import db
import stripe
import os
from flask import redirect
from .plans import get_plan_amount, get_credit_amount, get_plan_by_id_lang

def assign_credit(user, credits_to_add):
    user.credits += credits_to_add
    db.session.commit()

    return f"Added {credits_to_add} credits to user {user.id}", 200


def stripe_purchase(user, **kwargs):
    try:
        plan_id = kwargs.get('plan_id')
        if plan_id:
            amount = get_plan_amount(plan_id)
        
        credits_to_add = kwargs.get('credits')
        if credits_to_add:
            amount = get_credit_amount(credits_to_add)

        # Create a new checkout session
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=user.id if user.is_authenticated else None,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': get_plan_by_id_lang(plan_id, language=user.language),
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=os.environ['STRIPE_SUCCESS_URL'],
            cancel_url=os.environ['STRIPE_CANCEL_URL'],
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
