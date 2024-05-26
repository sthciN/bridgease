from models.models import ClientVisaPrograms, UserProfile
from db.database import db
from openai import OpenAI
from utils.user import get_user_info
from utils.locale.http_message import get_http_message
import json
from .assistant import prepare_assistant


def query_assistant(user_id, app):
    client = OpenAI()
    user_info = get_user_info(user_id, app)
    
    print('user_info', user_info)
    message = f"My_Information: {user_info}."
    assis_id = 'asst_4eCXf4UfzJtfPlhZBwRPcN2a'

    result = prepare_assistant(client, assis_id, message)

    print('<<>>', result)
    
    try:
        json_result = json.loads(result)
        data = json_result['data']
        if len(data) == 0:
            # Try again
            result = prepare_assistant(client, assis_id, message)
            json_result = json.loads(result)
    
    except Exception as e:
        print('error', e)
        assis_id = 'asst_vjyXRZTqnlFqG3DrbHt4RabK'
        json_result = prepare_assistant(client, assis_id, result)
        json_result = json.loads(json_result)
    
    json_result = json_result['data']
    print('END????', json_result)

    with app.app_context():
        user_profile = UserProfile.query.filter_by(users_id=user_id).first()

    # Translate the texts
    try:
        user_language = user_profile.language
        if user_language == 'en':
            raise Exception('No need to translate')
        
        assis_id = 'asst_5uBqYwJfUa09gMq6FEpUkFl6'

        print('user_language', user_language)
        result_translated = prepare_assistant(client, assis_id, f'Language: {user_language}. ' + str(json_result))
        json_result_translated = json.loads(result_translated)

        print('json_result_translated', json_result_translated)

    except Exception as e:
        print('>>>The translation error', e)
        json_result_translated = []
    
    with app.app_context():
        client_visa_program = ClientVisaPrograms(
            users_id=user_id,
            visa_programs=json.dumps(json_result),
            visa_program_translate=json.dumps(json_result_translated),
            is_latest=True
            )
        db.session.add(client_visa_program)
        db.session.commit()
        user_profile.credits -= 1
        db.session.commit()

    return json_result

def create_visa_assistant():
    client = OpenAI()
    model = "gpt-3.5-turbo"

    
    # Add file using vectore store 
    assistant = client.beta.assistants.create(
        name="Visa Assistant6 gpt3.5",
        instructions="""You are a great immigratoin advisor. You identify top 5 visa programs among data present in txt file that may align with My_Information. 
         Your answer must be in a JSON convertible format specified as: [{ "doc_id": 000000, "title": "", "country": "", "short_summary": "" }]. 
         The doc_id should be the doc_id of the visa program. The title should be the title of the visa program. The country should be the country of the visa program.
         The short_summary should be a brief description of My_Information and its alignement with the visa program but not more than 60 words.
         You try to find AT LEAST 2 visa programs that align with My_Information.
         You do not explain your answer and do not write any additional information.
         You only provide your answer in the JSON format specified above.""",
        model=model,
        tools=[{"type": "file_search"}],
        )
    vector_store = client.beta.vector_stores.create(name="Visa Programs")
    file_paths = ["./db/data.txt"]
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
    
    print(file_batch.status)
    print(file_batch.file_counts)
    
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    return None

def create_json_assistant():
    client = OpenAI()

    model = "gpt-3.5-turbo-1106"

    assistant = client.beta.assistants.create(
        name="JSON Assistant",
        instructions="""Export JSON from the provided content. The JSON should be in the following format:
        [{"doc_id": 000000, "title": "", "country": "Germany", "weight": 0.00, "short_summary": "", "long_summary": ""}]
        Do not explain your answer. 
        Do not provide any details except the JSON format. 
        If the data is not convertibale to JSON return an empty list. 
        Do not provide any additional information. 
        Do not write any more words that does not fit into the json format that I provided.
        The JSON format should be exactly as I provided.
        Do not contain any more words outside of the JSON. 
        I want to pass the JSON to an api, so it is important that I get a JSON format response following the sample I provided.
        """,
        model=model
    )
    assis_id = assistant.id
    print(assis_id)

    return None

def create_timeline_assistant():
    client = OpenAI()

    model = "gpt-3.5-turbo"
    # The actions could be from this list: ["Learn Language (English, Dutch, German, etc.)", "Pass Qualification Test", "Prepare Documents", "Find Sponsor", "Submit Documents", "Schedule Interview", "Interview", "Medical Examination", "Pay Fees", "Receive Visa"].
    # If user has an advance or native knowledge of the language of the visa program's country, they do not need to learn the language.
    # If the documents for the visa program take time, consider that time when generating the timeline for the user.
    # The Medical Exams are valid for a certain amount of time so consider adding it in a proper date in the timeline.
    assistant = client.beta.assistants.create(
        name="Timeline Assistant",
        instructions="""You are a professional immigration consultant. You are tasked with creating a timeline of the visa application process for a user.
        You must create a timeline that contains the "dates" and the "actions" that needs to be taken by the user. 
        The actions are from this list: ["Learn Language (English, Dutch, German, etc.)", "Pass Qualification Test", "Apply for Visa", "Prepare Documents", "Find Sponsor", "Submit Documents", "Schedule Interview", "Interview", "Medical Examination", "Pay Fees", "Receive Visa"].
        And the dates are in the format of "YYYY-MM-DD". 
        Try to find the best timeline that fits the visa program and the user's information.
        The timeline could be as long as you need to cover the actions reqiured for the visa or immigration plan.
        The timeline should make sense and be realistic.
        You do not need to explain your answer.
        You do not write any additional information.
        You provide your answer in the JSON format specified as: [{"date": "YYYY-MM-DD", "action": ""}].
        """,
        model=model
    )
    assis_id = assistant.id
    print(assis_id)

    return None

def create_timeline_json_assistant():
    client = OpenAI()

    model = "gpt-3.5-turbo"

    assistant = client.beta.assistants.create(
        name="Timeline JSON Assistant",
        instructions="""Extract a list of dictionaries from the message. 
        Do not forget to add all the items to the list. 
        The format comes as follow: {"data": [{"date": "", "action": ""}]}. 
        Finally return it as a JSON format.
        """,
        model=model
    )
    assis_id = assistant.id
    print(assis_id)

    return None
