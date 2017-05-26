from flask_restful import Resource, Api, abort
from flask import jsonify, make_response
from app.data.models import User


def abort_if_user_doesnt_exist(user_id):
    if User.query.filter_by(id=user_id).first() is None:
        abort(404, message="User not found.")


class RestfulApi(Resource):
    def get(self, id):
        if id == "all":
            users = User.query.all()
            json_users = {"users":[{"username": user.username, "first_name": user.jmeno} for user in users]}
            return make_response(jsonify(json_users))
        else:
            abort_if_user_doesnt_exist(id)
            user = User.query.filter_by(id=id).first()
            json_user = {"users": {"username": user.username, "first_name": user.jmeno}}
            return make_response(jsonify(json_user))
