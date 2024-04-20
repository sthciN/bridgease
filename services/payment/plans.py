from utils.locale.plan_message import get_plan_message

def get_plan_amount(plan_id):
    if plan_id == 1:
        amount = 50000  # amount in cents
    elif plan_id == 2:
        amount = 8000  # amount in cents
    elif plan_id == 3:
        amount = 10000  # amount in cents
    else:
        amount = 50000  # amount in cents

    return amount

def get_credit_amount(number_of_credits):
    amount = number_of_credits * 1000

    return amount

def get_plan_by_id_lang(plan_id, language):
    try:
        if plan_id == 1:
            return get_plan_message(language=language, get_plan_message="unlimited")
        elif plan_id == 2:
            return get_plan_message(language=language, get_plan_message="single_credit")
        elif plan_id == 3:
            return get_plan_message(language=language, get_plan_message="triple_credit")
        elif plan_id == 4:
            return get_plan_message(language=language, get_plan_message="credit_based")
        else:
            return get_plan_message(language=language, get_plan_message="unlimited")
    except:
        return get_plan_message(language=language, get_plan_message="unlimited")

    
def get_plan_ids():
    return [1, 2, 3, 4]
