from flask import Blueprint, make_response

error = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return make_response(jsonify({"Error": "Not Found"}), 404)
