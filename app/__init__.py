# import necessary for bare flask app
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

# application variables
app = Flask(__name__)
boostrap = Bootstrap(app)
app.config.from_object(Config)
# routes must be set after app variable is set
from app import routes
