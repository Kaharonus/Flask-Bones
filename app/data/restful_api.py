from flask_restful import Resource, Api, abort
from itsdangerous import TimestampSigner
from flask import jsonify, make_response, request, current_app
from app.data.models import User
import bcrypt as bcr


def abort_if_user_doesnt_exist(user_id):
    if User.query.filter_by(id=user_id).first() is None:
        abort(404, message="User not found.")

def abort_if_token_has_error(token = ""):
    default_token = TimestampSigner(current_app.config['SECRET_KEY'])

    if token == "" or token is None:
        abort(404, message='You haven\'t entered any token.')
    else:
        if User.query.filter_by(api_key=token).first() is None:
            abort(401, message='Token: ' + token + ' was not found.')
        elif default_token.unsign(token, max_age=current_app.config['API_TOKEN_EXPIRATION']):
            abort(401, message='Your token is no longer valid')
        else:
            return True


class RestfulApi(Resource):
    def get(self, id):
        abort_if_token_has_error(request.args.get('token'))
        abort_if_user_doesnt_exist(id)
        user = User.query.filter_by(id=id).first()
        json_user = {"users": {"username": user.username, "first_name": user.jmeno}}
        return make_response(jsonify(json_user))
