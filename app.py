from flask import Flask
from flask_jwt_extended import JWTManager
from flask_session import Session
from config import Config
from models import db
from auth import auth_bp
from routes import student_bp
from utils import create_response

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
jwt = JWTManager(app)
Session(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)

@app.route("/", methods=["GET"])
def home():
    return create_response(message="Welcome to the Student API")

if __name__ == "__main__":
    app.run(debug=True)
