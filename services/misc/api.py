from app import app, logger
from flask import Blueprint, jsonify
from db.database import db
from models.models import Country
from models.schemas import CountrySchema
import flask_praetorian
from utils.handler import NotFoundData
from utils.locale.http_message import get_http_message

misc_blueprint = Blueprint('misc_blueprint', __name__)

@app.route('/countries')
@flask_praetorian.auth_required
def get_countries():
    try:
        countries = Country.query.all()
        
        if not countries:
            raise NotFoundData(get_http_message(language='en', http_type='country_not_found'))
        
        countries = CountrySchema().dump(countries, many=True)
        
        return jsonify(countries), 200

    except NotFoundData as e:
        return jsonify({"error": str(e)}), 404
    
    except Exception as e:
        logger.error(e)
        return jsonify({"error": get_http_message(language='en', http_type='failed')}), 500
