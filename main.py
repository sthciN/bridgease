from app import app
from services.payment.purchase import payment_blueprint
from services.visa.visacard import visa_blueprint
from services.user.user_profile import user_blueprint

app.register_blueprint(payment_blueprint)
app.register_blueprint(visa_blueprint)
app.register_blueprint(user_blueprint)

@app.route("/")
def home():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
