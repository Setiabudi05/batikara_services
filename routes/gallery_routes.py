from flask import Blueprint, flash, redirect, render_template, request, jsonify, current_app, url_for
from bson import ObjectId
from models.gallery_model import gallery_serializer, create_gallery_data, update_gallery_data

gallery_bp = Blueprint('gallery', __name__)

# GET - Flutter API
@gallery_bp.route('/gallery', methods=['GET'])
def get_galleries():
    galleries = current_app.mongo.db.galeryBatik.find()
    return jsonify([gallery_serializer(g) for g in galleries]), 200

# INDEX - Web
@gallery_bp.route('/web/gallery')
def web_gallery_index():
    galleries = current_app.mongo.db.galeryBatik.find()
    return render_template('gallery/index.html', galleries=[gallery_serializer(g) for g in galleries])

# CREATE
@gallery_bp.route('/web/gallery/create', methods=['GET', 'POST'])
def web_gallery_create():
    if request.method == 'POST':
        image = request.files.get("image")

        if not image:
            flash("Image is required", "danger")
            return redirect(request.url)

        gallery_data = create_gallery_data(request.form, image)
        current_app.mongo.db.galeryBatik.insert_one(gallery_data)
        flash(" gallery berhasil ditambahkan!", "success")
        return redirect(url_for('gallery.web_gallery_index'))

    return render_template('gallery/create.html')

# EDIT
@gallery_bp.route('/web/gallery/edit/<id>', methods=['GET', 'POST'])
def web_gallery_edit(id):
    gallery = current_app.mongo.db.galeryBatik.find_one({"_id": ObjectId(id)})
    if not gallery:
        return "Not found", 404

    if request.method == 'POST':
        image = request.files.get("image")
        update_data = update_gallery_data(request.form, image)
        current_app.mongo.db.galeryBatik.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        flash("gallery berhasil diperbarui!", "success")
        return redirect(url_for('gallery.web_gallery_index'))

    return render_template('gallery/edit.html', gallery=gallery_serializer(gallery))

# DELETE
@gallery_bp.route('/web/gallery/delete/<id>', methods=['POST'])
def web_gallery_delete(id):
    current_app.mongo.db.galeryBatik.delete_one({"_id": ObjectId(id)})
    flash("Event berhasil dihapus!", "info")
    return redirect(url_for('gallery.web_gallery_index'))

