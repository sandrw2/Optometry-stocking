from flask import Flask
from models import db
from routes.patientOrder import pt_orders_bp  # your orders routes blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

db.init_app(app)
app.register_blueprint(pt_orders_bp)

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()  # drops tables if they exist
        db.create_all()  # creates tables if they don't exist
    app.run(debug=True)
