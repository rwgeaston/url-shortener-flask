import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)


@app.route('/')
def home():
    return 'POST {"url": "your url"} to /shorten_url to get back a short redirect URL.'
