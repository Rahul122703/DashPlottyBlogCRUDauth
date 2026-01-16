from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.mongo import posts
from bson import ObjectId
blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.json

    posts.insert_one({
        "title": data["title"],
        "content": data["content"],
        "author": user_id
    })

    return {"msg": "Post created"}

@blog_bp.route("/posts", methods=["GET"])
def get_posts():
    all_posts = list(posts.find())
    for p in all_posts:
        p["_id"] = str(p["_id"])
    return jsonify(all_posts)

@blog_bp.route("/posts/<post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    data = request.json

    post = posts.find_one({"_id": ObjectId(post_id)})

    if not post:
        return {"msg": "Post not found"}, 404

    # optional: only allow author to edit
    if post["author"] != user_id:
        return {"msg": "Unauthorized"}, 403

    posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {
            "title": data["title"],
            "content": data["content"]
        }}
    )

    return {"msg": "Post updated"}

from bson import ObjectId

@blog_bp.route("/posts/<post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()

    post = posts.find_one({"_id": ObjectId(post_id)})

    if not post:
        return {"msg": "Post not found"}, 404

    # Only author can delete
    if post["author"] != user_id:
        return {"msg": "Unauthorized"}, 403

    posts.delete_one({"_id": ObjectId(post_id)})

    return {"msg": "Post deleted"}
