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

def get_plan_by_id(plan_id):
    if plan_id == 1:
        return "Unlimited"
    elif plan_id == 2:
        return "Single Credit"
    elif plan_id == 3:
        return "Triple Credit"
    elif plan_id == 4:
        return "Credit-based"
    else:
        return "Credit-based"

    
def get_plan_ids():
    return [1, 2, 3, 4]
