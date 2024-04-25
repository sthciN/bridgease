from app import app
from services.payment.api import payment_blueprint
from services.visa.api import visa_blueprint
from services.user.api import user_blueprint
from services.misc.api import misc_blueprint

app.register_blueprint(payment_blueprint)
app.register_blueprint(visa_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(misc_blueprint)

@app.route("/")
def home():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
