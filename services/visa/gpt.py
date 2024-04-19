from models.models import VisaProgram
from db.database import db
from openai import OpenAI
from utils.user import get_user_info

def query_gpt():
    seed = 7865
    contexts = db.session.execute(db.select(VisaProgram)).scalars()
    context = '\n---\n'.join([c.description for c in contexts])
    openai_client = OpenAI()
    user_info = get_user_info(id)
    print('user_info', user_info)
    question = f"Question: Information: {user_info}"

    # prompt = "Identify the top 3 visa programs that closely align with the provided content and question. Return the results in JSON format as specified: " + \
    #     'Sample JSON format: [{"doc_id": 000000, "title": "", "country": "Germany", "weight": 0.00}]. \n' + \
    #     f"Context: {context} \n" + question
    
    # response = openai_client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     max_tokens=300,
    #     temperature=0.2,
    #     seed=seed,
    #     prompt=prompt
    # )
    # result = response.choices[0].text
    result = [{"doc_id": 000000, "title": "", "country": "Germany", "weight": 0.00}]

    return result
