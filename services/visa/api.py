from app import app
from flask import Blueprint, jsonify
from db.database import db
from models.models import UserProfile
from .gpt import query_gpt
from .assistant import query_assistant
import flask_praetorian
from utils.handler import NotFoundData, NotEnoughCredit
from utils.locale.http_message import get_http_message

visa_blueprint = Blueprint('visa_blueprint', __name__)

@app.route("/user/<int:id>/visacard")
@flask_praetorian.auth_required
def get_visacard(id):
    try:
        user = UserProfile.query.get(id)
        if not user:
            raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
        
        if user.credits < 1:
            raise NotEnoughCredit(get_http_message(language=user.language, http_type='not_enough_credits'))
        
        result = query_gpt()

        user.credits -= 1
        db.session.commit()

        return result

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/user/<int:id>/assistant")
# @flask_praetorian.auth_required
def get_visacard_by_assistant(id):
    try:
        user = UserProfile.query.get(id)
        if not user:
            raise NotFoundData(get_http_message(language='en', http_type='user_not_found'))
        if user.credits < 1:
            raise NotEnoughCredit(get_http_message(language=user.language, http_type='not_enough_credits'))
        
        result = query_assistant()

        user.credits -= 1
        db.session.commit()
        return result

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404

    except NotEnoughCredit as e:
        return jsonify({"error": str(e)}), 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
