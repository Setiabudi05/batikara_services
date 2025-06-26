from flask import Blueprint, render_template, redirect, url_for, request
from config import user_col
from bson.objectid import ObjectId

user_web = Blueprint("user_web", __name__)

# ========================
# Halaman Daftar User
# ========================
@user_web.route("/admin/user")
def user_index():
    users = list(user_col.find())
    return render_template("user/index.html", users=users)

# ========================
# Edit User (GET & POST)
# ========================
@user_web.route("/admin/user/edit/<id>", methods=["GET", "POST"])
def edit_user(id):
    user = user_col.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        user_col.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"username": username, "email": email}}
        )
        return redirect(url_for("user_web.user_index"))

    return render_template("user/edit.html", user=user)

# ========================
# Hapus User
# ========================
@user_web.route("/admin/user/delete/<id>")
def delete_user(id):
    user_col.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("user_web.user_index"))
