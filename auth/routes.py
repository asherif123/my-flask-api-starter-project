from ..models import User, UserSchema
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask import Blueprint
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = UserSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = User(**data)
    if user.email_already_registered():
        return jsonify({"error": "This email is already registered"}), 400
    user.save_to_db()
    return jsonify({"msg": "created sucsessfully", "User": UserSchema().dump(user)}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    error = UserSchema().validate(request.json, partial=("first_name", "last_name"))
    if error:
        return jsonify(error), 400

    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
