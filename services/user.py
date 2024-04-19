from app import app
from db.database import db
from models.models import Users, Client, UserProfile
from flask import request, jsonify
from services.auth.guard_app import guard

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

@app.route("/user", methods=["POST"])
def post_user():
    user = UserProfile(first_name="Ati", last_name="Bay", email="sth@sth.com", born_date="1990-01-01")
    db.session.add(user)
    db.session.commit()
    client = Client(user_profile_id=user.id, current_country_of_residence=14, citizenship_country=14)
    db.session.add(client)
    db.session.commit()
    return "OK"

@app.route("/user/<int:id>")
def get_user(id):
    # user = db.get_or_404(UserProfile, id)
    client = db.session.query(Client).filter(Client.user_profile_id == id).first()
    print('client', client)

    return "OK"