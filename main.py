from app import app
from services.payment.purchase import credit_blueprint
from services.visa.visacard import visa_blueprint

app.register_blueprint(credit_blueprint)
app.register_blueprint(visa_blueprint)

@app.route("/")
def home():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
