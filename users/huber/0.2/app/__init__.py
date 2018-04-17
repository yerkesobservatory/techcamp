from flask import Flask
#Setup flask webserver as "app"
app = Flask(__name__)
from app import routes
