from flask import Flask
from app.routes import bp  # import the blueprint

app = Flask(__name__)
app.register_blueprint(bp)  # ✅ Correct way to register routes
