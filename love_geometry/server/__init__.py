from flask import Flask
app = Flask(__name__)


@app.before_first_request
def import_views():
    import love_geometry.server.views  # noqa E402
