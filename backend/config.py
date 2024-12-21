from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS, cross_origin

# Configurations for two databases
class Config1:
    SQLALCHEMY_DATABASE_URI = "mysql://root:12345678@localhost/users"
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://chatbot-eight-umber-45.vercel.app" , "https://chatbot-git-main-vaibhavbarala26s-projects.vercel.app/" , "https://chatbot-sigma-rosy-81.vercel.app/" , "https://chatbot-vaibhavbarala26s-projects.vercel.app/" , "https://chatbot-vaibhavbarala26s-projects.vercel.app"], methods=["GET", "POST"], allow_headers=["Content-Type"])

# Add main database configuration
app.config.from_object(Config1)


app.config['SQLALCHEMY_ECHO'] = True  # Enable SQLAlchemy debug output

# Initialize SQLAlchemy
db = SQLAlchemy(app)

