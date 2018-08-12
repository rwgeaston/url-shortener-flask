from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return 'POST {"url": "your url"} to /shorten_url to get back a short redirect URL.'
