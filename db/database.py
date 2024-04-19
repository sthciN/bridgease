import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine, url
from app import app
from flask_migrate import Migrate

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
print("Database connected successfully")