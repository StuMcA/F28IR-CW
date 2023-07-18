from flask import Flask
from application import config

app = Flask(__name__)
app.config.update(**config.config)

from application import routes
