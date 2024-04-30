from app import app
from db.database import db
import json
from models.models import Users, Client, UserProfile, Country, IndustryType
from flask import request, jsonify, Blueprint
from services.auth.guard_app import guard
import flask_praetorian
from flask_praetorian.exceptions import MissingUserError, InvalidUserError

from utils.handler import NotFoundData, InvalidBodyRequest
from utils.locale.http_message import get_http_message
from models.schemas import UsersSchema, UserProfileSchema, ClientBasicInformationSchema, ClientFamilyInformationSchema, ClientBusinessInformationSchema, ClientPreferenceInformationSchema

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
        email = request.json.get("email").strip()
        password = request.json.get("password")
        language = request.json.get("language")
        if not email or not password:
            raise InvalidBodyRequest(get_http_message(language=language, http_type='invalid_body_request'))
        
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError(get_http_message(language=language, http_type='user_already_exists'))

        user = Users(email=email, hashed_password=guard.hash_password(password))
        db.session.add(user)
        db.session.commit()
        user_id = db.session.query(Users).filter_by(email=email).first().id
        print('IS there an id', user.id)
        print('NOW user_id', user_id)
        user_profile = UserProfile(users_id=user_id)
        db.session.add(user_profile)
        db.session.commit()
        ret = {"access_token": guard.encode_jwt_token(user)}
        
        print('ret', ret)
        
        return jsonify(ret), 200

    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400

    except ValueError as e:
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
        email = request.json.get("email").strip()
        password = request.json.get("password")
        if not email or not password:
            raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
        
        user = guard.authenticate(email, password)
        access_token = guard.encode_jwt_token(user)
        user = db.session.query(Users).filter_by(email=email).first()
        user = UsersSchema().dump(user)
        res = {'access_token': access_token, 'user': user}
        
        return jsonify(res), 200

    except InvalidBodyRequest as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user-profile', methods=['GET'])
@flask_praetorian.auth_required
def get_user_profile_by_access_token():    
    try:
        user_id = flask_praetorian.current_user().id
        user = Users.query.get(user_id)
        if not user:
            raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))

        user = UsersSchema().dump(user)
        
        print('user', user)
        
        return jsonify(user), 200

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user-personal-info', methods=['GET', 'PUT'])
@flask_praetorian.auth_required
def user_personal_info():
    if request.method == 'GET':
        try:
            try:
                current_user = flask_praetorian.current_user()
            
            except Exception as e:
                return jsonify(message='User not found or token is invalid'), 404
            
            user_id = current_user.id
            user = Users.query.get(user_id)
            if not user:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))

            email = user.email
            user_profile = UserProfile.query.filter_by(users_id=user_id).first()
            user_profile = UserProfileSchema().dump(user_profile)
            user_profile['email'] = email
            
            print('user_profile', user_profile)
            
            return jsonify(user_profile), 200
        
        
        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == 'PUT':
        try:
            user_id = flask_praetorian.current_user().id
            first_name = request.json.get('firstName')
            last_name = request.json.get('lastName')
            born_date = request.json.get('bornDate')
            phone = request.json.get('phone')

            # Find the user
            user_profile = UserProfile.query.filter_by(users_id=user_id).first()
            print('user_profile', user_profile)
            if not user_profile:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))

            user_profile.first_name = first_name.strip() if first_name else first_name
            user_profile.last_name = last_name.strip() if last_name else last_name
            user_profile.born_date = born_date
            user_profile.phone = phone.strip() if phone else phone
            # Commit the changes
            db.session.commit()

            return jsonify(get_http_message(language='en', http_type="user_personal_info_updated_successfully")), 200

        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


@app.route('/update_password', methods=['PUT'])
@flask_praetorian.auth_required
def update_password():
    try:
        user_id = request.json.get('user_id').strip()
        new_password = request.json.get('new_password')
        if not user_id or not new_password:
            raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

        # Find the user
        user = Users.query.get(user_id)
        if not user:
            raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))

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


@app.route('/client-basic-information', methods=['GET', 'PUT'])
@flask_praetorian.auth_required
def client_basic_information():
    if request.method == 'GET':
        try:
            user_id = flask_praetorian.current_user().id
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)
            
            client = ClientBasicInformationSchema().dump(client)
            return jsonify(client), 200

        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'PUT':
        try:
            user_id = flask_praetorian.current_user().id
            if not user_id:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
            
            print('json', request.json)
            current_country_of_residence = request.json.get('countryOfResidence')
            citizenship_country = request.json.get('countryOfCitizenship')
            education_type = request.json.get('fieldOfStudy')
            education_level = request.json.get('educationDegree')
            language_ability = request.json.get('languages')
            work_industry = request.json.get('workingIndustry') # not int but str
            years_of_work_experience = request.json.get('yearsOfExperience')

            if current_country_of_residence and not isinstance(current_country_of_residence, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            if not citizenship_country:
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            if not isinstance(citizenship_country, str):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

            if education_type and not isinstance(education_type, str):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            if education_level and not isinstance(education_level, str):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            if language_ability and not isinstance(language_ability, list):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            if work_industry and not isinstance(work_industry, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            if years_of_work_experience:
                if not isinstance(years_of_work_experience, (int, str)):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

                try:
                    years_of_work_experience = int(years_of_work_experience)
                    print('years_of_work_experience', years_of_work_experience)
                except Exception as e:
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            # create a row in Client table
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)

            # Update the password
            
            client.current_country_of_residence = current_country_of_residence
            client.citizenship_country = citizenship_country
            client.education_type = education_type
            client.education_level = education_level
            client.language_ability = json.dumps(language_ability) if language_ability else None
            client.work_industry = work_industry
            client.years_of_work_experience = years_of_work_experience

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


@app.route('/client-family-information', methods=['GET', 'PUT'])
@flask_praetorian.auth_required
def client_family_information():
    if request.method == 'GET':
        try:
            user_id = flask_praetorian.current_user().id
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)
            
            client = ClientFamilyInformationSchema().dump(client)
            return jsonify(client), 200

        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'PUT':
        try:
            user_id = flask_praetorian.current_user().id
            if not user_id:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
            
            print('json', request.json)
            marital_status = request.json.get('maritalStatus')
            number_of_dependant_accompanying = request.json.get('noOfDependentAccompanyingYou')
            military_service_status = request.json.get('militaryServiceStatus')
            has_criminal_record = request.json.get('haveCriminalRecord')

            if marital_status:
                if not isinstance(marital_status, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
                marital_status = marital_status.strip()
            
            if military_service_status:
                if not isinstance(military_service_status, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
                military_service_status = military_service_status.strip()
            
            if has_criminal_record:
                if not isinstance(has_criminal_record, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
                has_criminal_record = has_criminal_record.strip()
            
            if number_of_dependant_accompanying:
                if not isinstance(number_of_dependant_accompanying, (int, str)):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

                try:
                    number_of_dependant_accompanying = int(number_of_dependant_accompanying)
                    print('number_of_dependant_accompanying', number_of_dependant_accompanying)
                except Exception as e:
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            # create a row in Client table
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)

            # Update the password
            
            client.marital_status = marital_status
            client.number_of_dependant_accompanying = number_of_dependant_accompanying
            client.military_service_status = military_service_status
            client.has_criminal_record = has_criminal_record

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

@app.route('/user-business-information', methods=['GET', 'PUT'])
@flask_praetorian.auth_required
def client_business_information():
    if request.method == 'GET':
        try:
            user_id = flask_praetorian.current_user().id
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)
            
            client = ClientBusinessInformationSchema().dump(client)
            return jsonify(client), 200

        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'PUT':
        try:
            user_id = flask_praetorian.current_user().id
            if not user_id:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
            
            print('json', request.json)
            investment_capital_available_range = request.json.get('investmentCapitalAvailableRange')
            is_entrepreneur = request.json.get('isEntrepreneuer')

            if investment_capital_available_range:
                if not isinstance(investment_capital_available_range, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
                investment_capital_available_range = investment_capital_available_range.strip()
            
            if is_entrepreneur:
                if not isinstance(is_entrepreneur, str):
                    raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
                is_entrepreneur = is_entrepreneur.strip()

            # create a row in Client table
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)

            # Update the password
            client.investment_capital_available_range = investment_capital_available_range
            client.is_entrepreneur = is_entrepreneur

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

@app.route('/user-preference-information', methods=['GET', 'PUT'])
@flask_praetorian.auth_required
def client_preference_information():
    if request.method == 'GET':
        try:
            user_id = flask_praetorian.current_user().id
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)
            
            client = ClientPreferenceInformationSchema().dump(client)
            return jsonify(client), 200

        except NotFoundData as e:
            return jsonify({"error": str(e)}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'PUT':
        try:
            user_id = flask_praetorian.current_user().id
            if not user_id:
                raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
            
            print('json', request.json)
            preferred_climate_type = request.json.get('preferredClimate')
            preferred_language = request.json.get('preferredLanguage')
            preferred_living_cost_range = request.json.get('preferredLivingCostRange')
            preferred_industry = request.json.get('preferredIndustry')
            
            if preferred_climate_type and not isinstance(preferred_climate_type, list):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            if preferred_language and not isinstance(preferred_language, list):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

            if preferred_living_cost_range and not isinstance(preferred_living_cost_range, str):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))
            
            if preferred_industry and not isinstance(preferred_industry, str):
                raise InvalidBodyRequest(get_http_message(language='en', http_type='invalid_body_request'))

            # create a row in Client table
            client = Client.query.filter_by(users_id=user_id).first()

            if not client:
                client = Client(users_id=user_id)
                db.session.add(client)

            # Update the password
            client.preferred_climate_type = preferred_climate_type
            client.preferred_language = preferred_language
            client.preferred_living_cost_range = preferred_living_cost_range
            client.preferred_industry = preferred_industry
            
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
