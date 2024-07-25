from flask import Flask
from app import *

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

