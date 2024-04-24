from app import app
from flask import jsonify
from db.database import db

class NotFoundData(Exception):
    pass

class NotEnoughCredit(Exception):
    pass

class InvalidBodyRequest(Exception):
    pass


# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify({"error": "Resource not found"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()  # Rollback the session in case of database errors
#     return jsonify({"error": "Internal server error"}), 500
