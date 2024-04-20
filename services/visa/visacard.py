from app import app
from flask import Blueprint
from db.database import db
from models.models import UserProfile
from .gpt import query_gpt
import flask_praetorian
from utils.locale.error_message import get_error_message

visa_blueprint = Blueprint('visa_blueprint', __name__)

@app.route("/user/<int:id>/visacard")
@flask_praetorian.auth_required
def get_visacard(id):
    user = UserProfile.query.get(id)
    if user.credits < 1:
        return get_error_message(language=user.language, error_type='not_enough_credits'), 402
    
    result = query_gpt()

    user.credits -= 1
    db.session.commit()

    return result