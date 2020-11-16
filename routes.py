from .run import app
from .extensions import db
from flask import request, jsonify
import json
from .models import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


@app.route('/test_auth', methods=['GET'])
@jwt_required
def get_test_data():
    return jsonify({"msg": "you are logged in"}), 200
