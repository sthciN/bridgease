from app import app
from db.database import db
from models.models import Users, Client, UserProfile
from flask import request, jsonify, Blueprint
from services.auth.guard_app import guard
import flask_praetorian
from utils.locale.error_message import get_error_message

user_blueprint = Blueprint('user_blueprint', __name__)

@app.route("/register", methods=["POST"])
def register():
    """
    Registers a new user by parsing a POST request containing user credentials
    and storing them in the database.
    .. example::
       $ curl http://localhost:5000/register -X POST \
         -d '{"email":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)
    user = Users(email=email, hashed_password=guard.hash_password(password))
    db.session.add(user)
    db.session.commit()
    ret = {"access_token": guard.encode_jwt_token(user)}
    
    return jsonify(ret), 200

@app.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"email":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)
    user = guard.authenticate(email, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    
    return jsonify(ret), 200

@app.route('/update_password', methods=['PUT'])
@flask_praetorian.auth_required
def update_password():
    user_id = request.json.get('user_id')
    new_password = request.json.get('new_password')

    # Find the user
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": get_error_message(language='en', error_type='user_not_found')}), 404

    # Update the password
    user.hashed_password = guard.hash_password(new_password)

    # Commit the changes
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

@app.route('/update_user_profile', methods=['PUT'])
@flask_praetorian.auth_required
def update_user_profile():
    user_id = request.json.get('user_id')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    born_date = request.json.get('born_date')
    phone = request.json.get('phone')

    # Find the user
    user = UserProfile.query.get(users_id=user_id)
    if not user:
        return jsonify({"error": get_error_message(language='en', error_type='user_not_found')}), 404

    # Update the password
    user.first_name = first_name
    user.last_name = last_name
    user.born_date = born_date
    user.phone = phone
    # Commit the changes
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

@app.route('/update_client', methods=['PUT'])
@flask_praetorian.auth_required
def update_client():
    user_id = request.json.get('user_id')
    preferred_climate_type = request.json.get('preferred_climate_type')
    preferred_language = request.json.get('preferred_language')
    current_country_of_residence = request.json.get('current_country_of_residence')
    citizenship_country = request.json.get('citizenship_country')
    education_type = request.json.get('education_type')
    education_level = request.json.get('education_level')
    preferred_living_cost_range = request.json.get('preferred_living_cost_range')
    years_of_work_experience = request.json.get('years_of_work_experience')
    work_industry_id = request.json.get('work_industry_id')
    investment_capital_available_range = request.json.get('investment_capital_available_range')
    marital_status = request.json.get('marital_status')
    number_of_dependant_accompanying = request.json.get('number_of_dependant_accompanying')
    is_entrepreneur = request.json.get('is_entrepreneur')
    military_service_status = request.json.get('military_service_status')
    has_criminal_record = request.json.get('has_criminal_record')
    language_ability = request.json.get('language_ability')
    preferred_industry_id = request.json.get('preferred_industry_id')
    health_status = request.json.get('health_status')

    # Find the user
    user = Client.query.get(users_id=user_id)
    if not user:
        return jsonify({"error": get_error_message(language='en', error_type='user_not_found')}), 404

    # Update the password
    user.preferred_climate_type = preferred_climate_type
    user.preferred_language = preferred_language
    user.current_country_of_residence = current_country_of_residence
    user.citizenship_country = citizenship_country
    user.education_type = education_type
    user.education_level = education_level
    user.preferred_living_cost_range = preferred_living_cost_range
    user.years_of_work_experience = years_of_work_experience
    user.work_industry_id = work_industry_id
    user.investment_capital_available_range = investment_capital_available_range
    user.marital_status = marital_status
    user.number_of_dependant_accompanying = number_of_dependant_accompanying
    user.is_entrepreneur = is_entrepreneur
    user.military_service_status = military_service_status
    user.has_criminal_record = has_criminal_record
    user.language_ability = language_ability
    user.preferred_industry_id = preferred_industry_id
    user.health_status = health_status

    # Commit the changes
    db.session.commit()

    return jsonify({"message": "Client updated successfully"}), 200

