from flask import Blueprint, make_response, jsonify

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return make_response(jsonify({"error": "Not Found"}), 404)
