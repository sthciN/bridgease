def get_plan_message(language="en", plan_type="unlimited", **kwargs):

    try:
        error_messages = {
            "en": {
                "unlimited": "Unlimited",
                "single_credit": "Single Credit",
                "triple_credit": "Triple Credit",
                "credit_based": "Credit-based",
            },
            "tr": {
                "unlimited": "Sınırsız",
                "single_credit": "Tek Kredi",
                "triple_credit": "Üçlü Kredi",
                "credit_based": "Kredi tabanlı",
            },
            "fa": {
                "unlimited": "نامحدود",
                "single_credit": "یک اعتبار",
                "triple_credit": "سه اعتبار",
                "credit_based": "بر اساس اعتبار",
            }
        }

        return error_messages[language][plan_type]
    
    except:
        return "Unlimited"
