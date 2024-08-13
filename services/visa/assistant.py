import time
import logging

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
                return response
        
        except Exception as e:
            
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

def prepare_assistant(client, assis_id, message):
    thread = client.beta.threads.create()
    thread_id = thread.id

    client.beta.threads.messages.create(
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

    return result
