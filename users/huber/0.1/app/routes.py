from flask import render_template
from app import app

#Routes for Flask --Basicly the web address for Flask
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
