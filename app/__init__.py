from dotenv import find_dotenv, load_dotenv
from flask import Flask


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
app = Flask(__name__)
