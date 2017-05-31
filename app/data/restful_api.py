from flask_restful import Resource, Api, abort
from itsdangerous import TimestampSigner
from flask import jsonify, make_response, request, current_app
from app.data.models import User, Company
import bcrypt as bcr


def abort_if_company_doesnt_exist(company_id):
    if Company.find_by_id(company_id):
        abort(404, message="Company is not registered")


def abort_if_user_doesnt_exist(user_id):
    if User.query.filter_by(id=user_id).first() is None:
        abort(404, message="User not found.")


def abort_if_token_is_invalid(token = ""):
    # default_token = TimestampSigner(current_app.config['SECRET_KEY'])

    if token == "" or token is None:
        abort(404, message='No token provided.')
    elif Company.validate_api_key(token):
        abort(401, message="Company api key was not found or is no longer valid.")

    """else:
        if User.query.filter_by(api_key=api_key).first() is None:
            abort(401, message='Token: ' + api_key + ' was not found.')
        elif not default_token.unsign(api_key, max_age=current_app.config['API_TOKEN_EXPIRATION']):
            abort(401, message='Your api_key is no longer valid')
        else:
            return True"""


def abort_if_api_key_is_invalid(id, api_key = ""):
    if api_key == "" or api_key is None:
        abort(404, message="No api key provided with request.")
    elif Company.validate_api_key(id , api_key):
        abort(401, message="Api key not found.")
    else:
        return True


class RestfulApi(Resource):
    # logged user request
    def get(self, company_id, user_id):
        abort_if_company_doesnt_exist(company_id)
        abort_if_user_doesnt_exist(user_id)
        abort_if_api_key_is_invalid(company_id, request.args.get('api_key'))
        abort_if_token_is_invalid(request.args.get('token'))
        user = User.query.filter_by(id=id).first()
        json_user = {"users": {"username": user.username, "first_name": user.first_name, "token": user.token}}
        return make_response(jsonify(json_user))
