from app import app
from flask import Blueprint, request
from models.models import UserProfile
from .stripe_api import assign_credit, stripe_purchase
from .plans import get_plan_ids
import stripe
import os

credit_blueprint = Blueprint('credit_blueprint', __name__)


@app.route('/user/<int:id>/buy_plan', methods=['POST'])
def buy_plan(id):
    user = UserProfile.query.get(id)
    if not user:
        return "User not found", 404

    data = request.get_json()
    if not data or 'credits' not in data:
        return "Invalid request", 400
    
    try:
        if plan_id not in get_plan_ids():
            return "Invalid plan id", 400
        
        plan_id = int(data['plan_id'])
    
    except ValueError:
        return "Invalid plan id", 400


    # Create a charge: this will charge the user's card
    result = stripe_purchase(user, plan_id=plan_id)

    return result

@app.route('/user/<int:id>/add_credits', methods=['POST'])
def add_credits(id):
    user = UserProfile.query.get(id)
    if not user:
        return "User not found", 404

    data = request.get_json()
    if not data or 'credits' not in data:
        return "Invalid request", 400
    try:
        credits_to_add = int(data['credits'])
    except ValueError:
        return "Invalid number of credits", 400

    if 10 < credits_to_add < 1:
        return "Number of credits must be between 1 to 10", 400

    # Create a charge: this will charge the user's card
    result = stripe_purchase(user, credits=credits_to_add)

    return result

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ['STRIPE_ENDPOINT_SECRET']
    event = None

    stripe.api_key = os.environ["STRIPE_API_KEY"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return 'Invalid payload', 400
    
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Extract the user and credits from the session
        user = session['client_reference_id']
        credits_to_add = session['display_items'][0]['quantity']

        # Call the assign_credit function
        assign_credit(user, credits_to_add)

    return 'Success', 200
