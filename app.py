from flask import Flask
from app.routes import bp as main_bp
from app.admin_routes import admin_bp

app = Flask(__name__)
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)
