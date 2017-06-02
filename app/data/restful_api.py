from flask_restful import Resource, Api, abort
from itsdangerous import TimestampSigner
from flask_bcrypt import Bcrypt
from flask import jsonify, make_response, request, current_app
from app.data.models import User, Company, Application


def abort_if_company_doesnt_exist(company_id):
    if Company.find_by_id(company_id):
        abort(404, message="Company is not registered")


def abort_if_user_doesnt_exist(username):
    if User.query.filter_by(username=username).first() is None:
        abort(404, message="User not found.")


def abort_if_token_is_invalid(token=""):
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


"""def abort_if_api_key_is_invalid(id, api_key=""):
    if api_key == "" or api_key is None:
        abort(404, message="No api key provided with request.")
    elif Company.validate_api_key(id, api_key):
        abort(401, message="Api key not found.")
    else:
        return True"""


class Token:

    def __init__(self, username):
        self.token = self.generate_token(username)
        self.max_age = current_app.config['TOKEN_EXPIRATION']

    def generate_token(self, username):
        hash = TimestampSigner(current_app.config['SECRET_KEY'])
        token = hash.sign(username)
        return str(token, 'utf-8')

    def set_max_age(self, max_age):
        self.max_age=max_age

    @staticmethod
    def validate_token(max_age, token=""):
        default_token = TimestampSigner(current_app.config['SECRET_KEY'])
        if token=="" or token is None:
            return False
        if not default_token.unsign(token, max_age=max_age):
            return False
        return True


class RestfulApiLogin(Resource):
    # logged user request
    def get(self):
        username = request.args.get('username')
        if Application.validate_api_key(request.args.get('api_key')):
            abort_if_user_doesnt_exist(username)
            user = User.query.filter_by(username=username).first()
            if user.check_password(request.args.get('password')):
                token = Token(username)
                if request.args.get('expiration') is not None:
                    token.set_max_age(int(request.args.get('expiration')))
                json_user = {"user": {"username": user.username, "first_name": user.first_name, "token":{"token": token.token, "expiration": token.max_age}}}
                return make_response(jsonify(json_user))
            else:
                return abort(401, message="Wrong password")
        else:
            return make_response("Invalid request")
        """abort_if_api_key_is_invalid(company_id, request.args.get('api_key'))

        nbejaka_funkce(request.args.get('username'), request.args.get('password'), request.args.get('api_key'))
        if(Token.validate_token())
        user = User.query.filter_by(id=id).first()
        json_user = {"users": {"username": user.username, "first_name": user.first_name, "token": user.token}}
        return make_response(jsonify(json_user))"""

#Dont know proper name for this class yet, should validate every request from logged user
class RestfulApiValidate(Resource):

    def get(self):
        token = request.args.get('token')
        max_age = request.args.get('expiration')
        if max_age is None:
            max_age = current_app.config['TOKEN_EXPIRATION']
        if Token.validate_token(int(max_age), token):
            return True
        else:
            return False
