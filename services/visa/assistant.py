from models.models import VisaProgram
from db.database import db
import os
from openai import OpenAI
from utils.user import get_user_info
import time
import logging
from datetime import datetime

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=3):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                
                # Get the last message in the thread
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                return response
        
        except Exception as e:
            
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


def query_assistant():
    seed = 7865
    contexts = db.session.execute(db.select(VisaProgram)).scalars()
    context = '\n---\n'.join([c.description for c in contexts])
    # print('context', context)
    client = OpenAI()
    user_info = get_user_info(id)
    print('user_info', user_info)
    # message = "Information: {'name': 'Asad', 'age': 30, 'country_citizenship': 'Iraq', 'country_residence': 'Iraq', 'preferred_language': 'English'}"
    message = f"Information: {user_info}"
    model = "gpt-4-1106-preview"


    # Create a new assistant
    # filepath = "./db/visa_file.txt"
    # file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")
    # assistant = client.beta.assistants.create(
    #     name="Visa Assistant",
    #     instructions="""Identify the top 3 visa programs that closely align with the provided content and question. Return the results in JSON format as specified: 
    #     Sample JSON format: [{"doc_id": 000000, "title": "", "country": "Germany", "weight": 0.00}]. 
    #     Do not explain your answer. Do not provide any details except the JSON format. If there is not a match return an empty list. Do not provide any additional information.""",
    #     tools=[{"type": "retrieval"}],
    #     model=model,
    #     file_ids=[file_object.id],
    # )
    # assis_id = assistant.id

    assis_id = 'asst_J3GseHs4tL4V4jNspVH1HxW4'
    print(assis_id)
    
    thread = client.beta.threads.create()
    thread_id = thread.id
    print(thread_id)

    print('*'*10)
    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content = message,
    )

    run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assis_id,
    )

    result = wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id, 
        run_id=run.id,
        )
    print(f"Run Steps --> {run_steps.data[0]}")

    return []
