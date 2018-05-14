from flask import Flask
from config import Config
#Setup flask webserver as "app"
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
