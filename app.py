from flask import Flask
from datetime import datetime
import pytz
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import Config
from routes.auth_web import auth_web_bp
from routes.google_oauth import google_auth_bp
from routes.article_routes import article_bp
from routes.gallery_routes import gallery_bp
from routes.favorite_routes import favorite_bp
from routes.user_routes import user_bp
from routes.dashboard_routes import dashboard_bp
from routes.event_routes import event_bp
import os 


# Setup zona waktu Jakarta
jakarta_tz = pytz.timezone("Asia/Jakarta")

app = Flask(__name__)


# # ✅ Tambahkan konfigurasi upload folder
# app.config['UPLOAD_FOLDER_GALLERY'] = os.path.join('static', 'uploads', 'gallery')
# os.makedirs(app.config['UPLOAD_FOLDER_GALLERY'], exist_ok=True)

# app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'articles')
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# app.config['UPLOAD_FOLDER_ARTICLES'] = os.path.join('static', 'uploads', 'articles')
# os.makedirs(app.config['UPLOAD_FOLDER_ARTICLES'], exist_ok=True)


app.config.from_object(Config)


# Inisialisasi Flask Extensions
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Inject objek ke app
app.mongo = mongo
app.jwt = jwt
app.bcrypt = bcrypt
app.mail = mail


# @app.template_filter('datetimeformat')
# def datetimeformat(value, format="%d/%m/%Y %H:%M"):
#     if isinstance(value, datetime):
#         value = value.astimezone(jakarta_tz)
#         return value.strftime(format)
#     return value


# Daftarkan semua blueprint
app.register_blueprint(auth_web_bp)
app.register_blueprint(google_auth_bp)
app.register_blueprint(article_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(user_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(event_bp)



# Run server Flask
if __name__ == '__main__':
    app.run(debug=True)
