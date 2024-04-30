from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
import logging

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

CORS(app)
logger = logging.getLogger(__name__)
