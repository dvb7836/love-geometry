from flask import Flask
from love_geometry.server import api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="")
