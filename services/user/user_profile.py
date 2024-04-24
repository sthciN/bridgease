from app import app
from db.database import db
from models.models import Users, Client, UserProfile
from flask import request, jsonify, Blueprint
from services.auth.guard_app import guard
import flask_praetorian
from utils.handler import NotFoundData, InvalidBodyRequest
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
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            raise InvalidBodyRequest(get_error_message(language='en', error_type='invalid_body_request'))

        user = Users(email=email, hashed_password=guard.hash_password(password))
        db.session.add(user)
        db.session.commit()
        ret = {"access_token": guard.encode_jwt_token(user)}
    
        return jsonify(ret), 200

    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"email":"Walter","password":"calmerthanyouare"}'
    """
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            raise InvalidBodyRequest(get_error_message(language='en', error_type='invalid_body_request'))
        
        user = guard.authenticate(email, password)
        ret = {"access_token": guard.encode_jwt_token(user)}
        
        return jsonify(ret), 200

    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_password', methods=['PUT'])
@flask_praetorian.auth_required
def update_password():
    try:
        user_id = request.json.get('user_id')
        new_password = request.json.get('new_password')
        if not user_id or not new_password:
            raise InvalidBodyRequest(get_error_message(language='en', error_type='invalid_body_request'))

        # Find the user
        user = Users.query.get(user_id)
        if not user:
            raise NotFoundData(get_error_message(language='en', error_type='user_not_found'))

        # Update the password
        user.hashed_password = guard.hash_password(new_password)

        # Commit the changes
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200
    
    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/update_user_profile', methods=['PUT'])
@flask_praetorian.auth_required
def update_user_profile():
    try:
        user_id = request.json.get('user_id')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        born_date = request.json.get('born_date')
        phone = request.json.get('phone')

        if not user_id:
            raise InvalidBodyRequest(get_error_message(language='en', error_type='invalid_body_request'))

        # Find the user
        user = UserProfile.query.get(users_id=user_id)
        if not user:
            raise NotFoundData(get_error_message(language='en', error_type='user_not_found'))

        # Update the password
        user.first_name = first_name
        user.last_name = last_name
        user.born_date = born_date
        user.phone = phone
        # Commit the changes
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/update_client', methods=['PUT'])
@flask_praetorian.auth_required
def update_client():
    try:
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

        if (not user_id or
            (user_id and
            (not preferred_climate_type
            and not preferred_language
            and not current_country_of_residence
            and not citizenship_country
            and not education_type
            and not education_level
            and not preferred_living_cost_range
            and not years_of_work_experience
            and not work_industry_id
            and not investment_capital_available_range
            and not marital_status
            and not number_of_dependant_accompanying
            and not is_entrepreneur
            and not military_service_status
            and not has_criminal_record
            and not language_ability
            and not preferred_industry_id
            and not health_status))):
            raise InvalidBodyRequest(get_error_message(language='en', error_type='invalid_body_request'))
        
        # Find the user
        user = Client.query.get(users_id=user_id)
        if not user:
            raise NotFoundData(get_error_message(language='en', error_type='user_not_found'))

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

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
