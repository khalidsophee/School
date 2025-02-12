from flask import Flask
from config import Config
from models import db
from utils import create_response  # Import this here
from routes import student_bp  # Import routes after defining app

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(student_bp)

@app.route("/", methods=["GET"])
def home():
    return create_response(message="Welcome to the Student API")

if __name__ == "__main__":
    app.run(debug=True)
