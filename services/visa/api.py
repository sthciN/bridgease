from app import app
from flask import Blueprint, jsonify, request
from db.database import db
from models.models import UserProfile, Users, ClientVisaPrograms, ClientVisaTimeline
from .visa_card import query_assistant
from .timeline import get_visa_timeline
import flask_praetorian
from utils.const import WEBSITE_LANGUAGES
from models.schemas import (ClientVisaProgramsSchema, 
            ClientVisaProgramByIDSchema, 
            ClientVisaProgramByIDTranslateSchema,
            ClientVisaTimelineSchema, 
            ClientVisaTimelineTranslateSchema, 
            ClientVisaProgramsTranslateSchema
            )
from utils.handler import NotFoundData, NotEnoughCredit
from utils.locale.http_message import get_http_message
from threading import Thread


visa_blueprint = Blueprint('visa_blueprint', __name__)

@app.route("/user/create_timeline_assistant")
def create_the_visa_assistant():
    # create_timeline_json_assistant()
    return jsonify({"message": "Visa assistant created successfully."}), 200

@app.route("/user/reprocess-visa-card")
@flask_praetorian.auth_required
def reprocess_visa_card():
    try:
        try:
            current_user = flask_praetorian.current_user()
        
        except Exception as e:
            return jsonify(message='User not found or token is invalid'), 404
        
        user_id = current_user.id
        client_visa_program = ClientVisaPrograms.query.filter_by(users_id=user_id, is_latest=True).first()
        
        if client_visa_program:
            # Remove the latest visa program
            client_visa_program.is_latest = False
            db.session.commit()

        user_profile = UserProfile.query.filter_by(users_id=user_id).first()
    
        if user_profile.credits < 1:
            raise NotEnoughCredit(get_http_message(language=user_profile.language, http_type='not_enough_credits'))
    
        # user_id = 33

        thread = Thread(target=query_assistant, args=(user_id, app))
        thread.start()

        return jsonify({"message": "Processing visa card..."}), 202

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/user/process-visa-card")
@flask_praetorian.auth_required
def process_visa_card():
    try:
        try:
            current_user = flask_praetorian.current_user()
        
        except Exception as e:
            return jsonify(message='User not found or token is invalid'), 404
        
        language = request.args.get('language')
        language = language if language in WEBSITE_LANGUAGES[1:] else None
        user_id = current_user.id

        client_visa_program = ClientVisaPrograms.query.filter_by(users_id=user_id, is_latest=True).first()
        
        if client_visa_program:
            if language:
                client_visa_program = ClientVisaProgramsTranslateSchema().dump(client_visa_program)
                return jsonify(client_visa_program), 200

            client_visa_program = ClientVisaProgramsSchema().dump(client_visa_program)
            return jsonify(client_visa_program), 200
    
        user_profile = UserProfile.query.filter_by(users_id=user_id).first()
    
        if user_profile.credits < 1:
            raise NotEnoughCredit(get_http_message(language=user_profile.language, http_type='not_enough_credits'))
    
        # user_id = 33

        # TODO Task queue instead of thread
        thread = Thread(target=query_assistant, args=(user_id, app))
        thread.start()

        return jsonify({"message": "Processing visa card..."}), 202

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/user/visa-card")
@flask_praetorian.auth_required
def get_visacards():
    try:
        current_user = flask_praetorian.current_user()
    
    except Exception as e:
        return jsonify(message='User not found or token is invalid'), 404
    
    user_id = current_user.id
    client_visa_program = ClientVisaPrograms.query.filter_by(users_id=user_id, is_latest=True).first()
    
    if not client_visa_program:
        return jsonify({"message": "Visa card not available yet."}), 202
    
    language = request.args.get('language')
    language = language if language in WEBSITE_LANGUAGES[1:] else None
    
    if language:
        client_visa_program = ClientVisaProgramsTranslateSchema().dump(client_visa_program)
    
    else:
        client_visa_program = ClientVisaProgramsSchema().dump(client_visa_program)
    
    return jsonify(client_visa_program), 200

@app.route("/user/process-timeline/<string:id>")
@flask_praetorian.auth_required
def process_timeline(id):
    try:
        try:
            id = int(id)
        except ValueError:
            return jsonify({'error': 'Invalid ID'}), 400

        try:
            current_user = flask_praetorian.current_user()
        
        except Exception as e:
            return jsonify(message='User not found or token is invalid'), 404
        
        user_id = current_user.id
        client_visa_timeline = ClientVisaTimeline.query.filter_by(users_id=user_id, doc_id=id, is_latest=True).first()
        
        language = request.args.get('language')
        language = language if language in WEBSITE_LANGUAGES[1:] else None

        if client_visa_timeline:
            if language:
                client_visa_timeline = ClientVisaTimelineTranslateSchema().dump(client_visa_timeline)
                return jsonify(client_visa_timeline), 200
            
            client_visa_timeline = ClientVisaTimelineSchema().dump(client_visa_timeline)
            return jsonify(client_visa_timeline), 200
        
        user_profile = UserProfile.query.filter_by(users_id=user_id).first()
        
        if user_profile.credits < 1:
            raise NotEnoughCredit(get_http_message(language=user_profile.language, http_type='not_enough_credits'))
        
        # user_id = 33

        thread = Thread(target=get_visa_timeline, args=(user_id, id, app))
        thread.start()

        return jsonify({"message": "Processing visa card..."}), 202

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/user/timeline/<string:id>")
@flask_praetorian.auth_required
def get_timeline(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'error': 'Invalid ID'}), 400

    try:
        current_user = flask_praetorian.current_user()
    
    except Exception as e:
        return jsonify(message='User not found or token is invalid'), 404
    
    user_id = current_user.id
    
    client_visa_timeline = ClientVisaTimeline.query.filter_by(users_id=user_id, doc_id=id, is_latest=True).first()
    
    if not client_visa_timeline:
        return jsonify({"timeline": []}), 202
    
    language = request.args.get('language')
    language = language if language in WEBSITE_LANGUAGES[1:] else None
    
    if language:
        client_visa_timeline = ClientVisaTimelineTranslateSchema().dump(client_visa_timeline)
    
    else:
        client_visa_timeline = ClientVisaTimelineSchema().dump(client_visa_timeline)
    
    return jsonify(client_visa_timeline), 200

@app.route("/user/visa-program/<string:id>")
@flask_praetorian.auth_required
def get_visacard_by_id(id):
    try:
        try:
            id = int(id)
        
        except ValueError:
            return jsonify({'error': 'Invalid ID'}), 400

        try:
            current_user = flask_praetorian.current_user()
        
        except Exception as e:
            return jsonify(message='User not found or token is invalid'), 404
        
        user_id = current_user.id
        
        client_visa_programs = ClientVisaPrograms.query.filter_by(users_id=user_id, is_latest=True).first()
        
        if not client_visa_programs:
            return jsonify({"visaProgram": ""}), 200
        
        language = request.args.get('language')
        language = language if language in WEBSITE_LANGUAGES[1:] else None

        if language:
            client_visa_program = ClientVisaProgramByIDTranslateSchema(doc_id=id).dump(client_visa_programs)

        else:
            client_visa_program = ClientVisaProgramByIDSchema(doc_id=id).dump(client_visa_programs)
                
        return jsonify(client_visa_program), 200
    
    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
