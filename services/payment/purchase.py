from app import app
from flask import Blueprint, request, jsonify
from models.models import UserProfile
from .stripe_api import assign_credit, stripe_purchase
from .plans import get_plan_ids
from utils.handler import NotFoundData, InvalidBodyRequest
import flask_praetorian
import stripe
import os
from utils.locale.error_message import get_error_message

payment_blueprint = Blueprint('payment_blueprint', __name__)

@app.route('/user/<int:id>/buy_plan', methods=['POST'])
def buy_plan(id):
    """
    Buy a plan by parsing a POST request containing the plan_id and user_id
    """
    try:
        user = UserProfile.query.get(users_id=id)
        if not user:
            raise NotFoundData(get_error_message(language='en', error_type='user_not_found'))

        plan_id = request.josn.get('plan_id')
        if not plan_id or plan_id not in get_plan_ids():
            raise InvalidBodyRequest(get_error_message(language=user.language, error_type='invalid_request'))
        
        plan_id = int(plan_id)

        # Create a charge: this will charge the user's card
        result = stripe_purchase(user, plan_id=plan_id)

        return result
    
    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/<int:id>/add_credits', methods=['POST'])
@flask_praetorian.auth_required
def add_credits(id):
    """
    Add credits to a user account by parsing a POST request containing the number of credits to add
    """
    try:
        user = UserProfile.query.get(users_id=id)
        if not user:
            raise NotFoundData(get_error_message(language='en', error_type='user_not_found'))

        credits = request.json.get('credits')
        if not credits:
            raise InvalidBodyRequest(get_error_message(language=user.language, error_type='invalid_request'))
        
        try:
            credits_to_add = int(credits)
        
        except ValueError:
            raise InvalidBodyRequest(get_error_message(language=user.language, error_type='invalid_number_of_credits'))

        if 10 < credits_to_add < 1:
            raise InvalidBodyRequest(get_error_message(language=user.language, error_type='number_of_credits_must_be_between_1_to_10'))

        # Create a charge: this will charge the user's card
        result = stripe_purchase(user, credits=credits_to_add)

        return result
    
    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        return get_error_message(language='en', error_type='invalid_payload'), 400
    
    except stripe.error.SignatureVerificationError as e:
        return get_error_message(language='en', error_type='invalid_signature'), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Extract the user and credits from the session
        user = session['client_reference_id']
        credits_to_add = session['display_items'][0]['quantity']

        # Call the assign_credit function
        assign_credit(user, credits_to_add)

    return 'Success', 200
