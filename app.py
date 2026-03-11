from flask import Flask
from config import Config
from models import db
from auth import auth
from notes import notes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(notes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)