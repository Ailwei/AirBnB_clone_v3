#!/usr/bin/python3
"""
error page
"""
from flask import Flask
from models import storage
from flask import Blueprint
from api.v1.views import app_views
from werkzeug.exceptions import NotFound
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """
    teardoen method
    """
    storage.close()


def handle_not_found_error(e):
    """
    handle not found error
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if '__name__' == '__main__':
    """
    main function
    """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    if not host:
        host = '0.0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
