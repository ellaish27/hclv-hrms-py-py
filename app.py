# app.py
from flask import Flask, send_from_directory, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Load secrets (PythonAnywhere uses this pattern)
try:
    import secrets
    DB_USER = secrets.DB_USER
    DB_PASS = secrets.DB_PASS
    DB_HOST = secrets.DB_HOST
    DB_NAME = secrets.DB_NAME
    JWT_SECRET = secrets.JWT_SECRET
    GMAIL_USER = secrets.GMAIL_USER
    GMAIL_APP_PASSWORD = secrets.GMAIL_APP_PASSWORD
except ImportError:
    # Fallback for local dev
    from dotenv import load_dotenv
    load_dotenv()
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    JWT_SECRET = os.getenv('JWT_SECRET')
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = JWT_SECRET

    # Initialize extensions
    from flask_sqlalchemy import SQLAlchemy
    from models import db
    db.init_app(app)

    JWTManager(app)
    CORS(app)

    # Register routes
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.hr import hr_bp
    from routes.employee import employee_bp

    app.register_blueprint(auth_bp, url -> prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(hr_bp, url_prefix='/api/hr')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')

    # Serve frontend
    @app.route('/')
    def index():
        return render_template('index.html')  # Redirects to /static/index.html

    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    return app

application = create_app()  # ← PythonAnywhere looks for "application"
