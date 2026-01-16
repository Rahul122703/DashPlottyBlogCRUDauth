from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db.mongo import users
from auth.utils import hash_password, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if users.find_one({"email": data["email"]}):
        return {"msg": "User exists"}, 400

    users.insert_one({
        "email": data["email"],
        "password": hash_password(data["password"])
    })

    return {"msg": "Registered successfully"}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    if not user or not check_password(data["password"], user["password"]):
        return {"msg": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user["_id"]))
    return jsonify(access_token=token)
