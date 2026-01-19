from flask import Flask
from flask_login import LoginManager
from database import db
from models import User
from routes import routes

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school_food.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Кошечки картошечки. Лишнева не скажут

login_manager = LoginManager(app)
login_manager.login_view = "routes.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
