from flask import Flask, request
from flask_cors import CORS

from config import *
from services.tracking.rest_controllers import tracking

import services

app = Flask(__name__)
app.register_blueprint(tracking, url_prefix='/tracking')
CORS(app)