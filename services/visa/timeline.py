from .assistant import prepare_assistant
from openai import OpenAI
from db.database import db
from models.models import ClientVisaTimeline, VisaProgram, UserProfile
from models.schemas import VisaProgramSchema
from utils.user import get_user_info
import json
from datetime import date

def get_visa_timeline(user_id, id, app):
    client = OpenAI()
    user_info = get_user_info(user_id, app)
    
    print('user_info', user_info)
    with app.app_context():
        visa_program = VisaProgram.query.filter_by(doc_id=id).first()
        visa_program = VisaProgramSchema().dump(visa_program)

    # today's date
    today = str(date.today())
    message = f"Todays' date: {today}, Visa Program: {visa_program} End of Visa Program Data.\n User Data: {user_info}"
    assis_id = 'asst_zpZnOfVBBrOcyKrYHZ1ooso9'

    result = prepare_assistant(client, assis_id, message)

    try:
        json_result = json.loads(result)
        print('::::::::::::FIRST TIME TIMELINE json_result', type(json_result), json_result)
        if len(json_result) == 0:
            print('no result??')
            # Try again
            result = prepare_assistant(client, assis_id, message)
            json_result = json.loads(result)
    
    except Exception as e:
        print('error', e)
        
        assis_id = 'asst_P0ViTFw8nD2rr9vgzpqhlapP'
        
        json_result = prepare_assistant(client, assis_id, result)

        print('json_result', type(json_result), json_result)
    
    json_result = json_result['data']
    print('END????', json_result)

    with app.app_context():
        user_profile = UserProfile.query.filter_by(users_id=user_id).first()
    
    # Translate the texts
    try:
        user_language = user_profile.language
        if user_language == 'en':
            raise Exception('No need to translate')
        
        assis_id = 'asst_JGRSYqgarnILUKx0wHMZ6AZd'

        print('user_language', user_language)
        result_translated = prepare_assistant(client, assis_id, f'Language: {user_language}. ' + str(json_result))
        json_result_translated = json.loads(result_translated)

        print('json_result_translated', json_result_translated)

    except Exception as e:
        print('>>>The translation error', e)
        json_result_translated = []

    with app.app_context():
        client_timeline = ClientVisaTimeline(
            users_id=user_id, 
            doc_id=id,
            timeline=json.dumps(json_result),
            timeline_translate=json.dumps(json_result_translated),
            is_latest=True
            )
        db.session.add(client_timeline)
        db.session.commit()
        user_profile.credits -= 1
        db.session.commit()

    return json_result