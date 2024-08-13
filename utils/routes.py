route = {
    "user": {
        "auth": {
            "register": "/register",
            "login": "/login",
            "logout": "/logout",
            "update-password": "/update_password",
            "refesh-token": "/user/refresh-token",
        },
        "language": "/user/language",
        "profile": "/user-profile",
        "profile-info": "/user-personal-info",
        "forms": {
            "basic-info": "/client-basic-information",
            "family-info": "/client-family-information",
            "business-info": "/user-business-information",
            "preference-info": "/user-preference-information",
        }
    },
    "visa": {
        "create-timeline-assistant": "/user/create_timeline_assistant",
        "reprocess-visa-card": "/user/reprocess-visa-card",
        "process-visa-card": "/user/process-visa-card",
        "visa-card": "/user/visa-card",
        "process-timeline/<string:id>": "/user/process-timeline/<string:id>",
        "timeline/<string:id>": "/user/timeline/<string:id>",
        "visa-program/<string:id>": "/user/visa-program/<string:id>",
    },
    "credit":
    {
        "bu-plan": "/user/<int:id>/buy_plan",
        "add-credit": "/user/<int:id>/add_credits",
        "stripe": "/webhook"
    },
    "misc": {
        "countries": "/countries"
    }
}