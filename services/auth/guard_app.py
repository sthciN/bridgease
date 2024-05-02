import os
from app import app
from flask_praetorian import Praetorian
import flask_cors
from models.models import Users

cors = flask_cors.CORS()
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}
guard = Praetorian()
guard.init_app(app, Users)
cors.init_app(app)
