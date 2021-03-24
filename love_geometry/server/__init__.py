from flask import Flask
app = Flask(__name__)

import love_geometry.server.views  # noqa E402
