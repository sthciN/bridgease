import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import url
from flask import jsonify
from sqlalchemy import text
from app import app
from flask_migrate import Migrate
from sqlalchemy.orm import Session


db = SQLAlchemy()
db_url = url.URL('postgresql',
            username=os.environ['DB_USER'],
            port = os.environ['DB_PORT'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            query={"client_encoding": "utf8"})

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()

# try:
#     session = Session(bind=db.engine)
#     session.execute(text('SELECT 1'))
#     # Perform a simple query to check the database connection
#     session.close()
#     print("Database connected successfully")

# except OperationalError:
#     print("Failed to connect to database")
#     raise RuntimeError("Failed to connect to database")


# @app.errorhandler(OperationalError)
# def handle_operational_error(error):
#     return jsonify({"error": "A server error occurred. Please try again later."}), 500
