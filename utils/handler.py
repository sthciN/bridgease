from old.app import app
from flask import Response, json
from utils.constants import FAILED_DATA, NOT_FOUND_DATA

class NotFoundData(Exception):
    pass


@app.errorhandler(Exception)
def handle_exception(e):
    response = Response()
    response.data = json.dumps(FAILED_DATA)
    response.content_type = "application/json"
    response.status_code = 500
    print(e)
    
    return response


@app.errorhandler(NotFoundData)
def handle_exception(e):
    response = Response()
    response.data = json.dumps(NOT_FOUND_DATA)
    response.content_type = "application/json"
    response.status_code = 404
    
    return response
