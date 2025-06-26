import os
from werkzeug.utils import secure_filename
from flask import current_app, request

# ✅ Tambahkan serializer ini
def gallery_serializer(gallery):
    image_path = gallery.get("image", "").replace("\\", "/")
    full_image_url = f"{request.host_url.rstrip('/')}{image_path}"
    return {
        "id": str(gallery["_id"]),
        "nama_batik": gallery.get("nama_batik", ""),
        "deskripsi": gallery.get("deskripsi", ""),
        "image": full_image_url
    }

# ✅ Buat galeri baru
def create_gallery_data(form, image_file):
    filename = secure_filename(image_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER_GALLERY']
    image_path = os.path.join(upload_folder, filename)
    image_file.save(image_path)

    relative_path = os.path.relpath(image_path, 'static').replace("\\", "/")
    image_url = f"/static/{relative_path}"

    return {
        "nama_batik": form.get("nama_batik"),
        "deskripsi": form.get("deskripsi"),
        "image": image_url
    }

# ✅ Update galeri
def update_gallery_data(form, image_file=None):
    update_data = {
        "nama_batik": form.get("nama_batik"),
        "deskripsi": form.get("deskripsi")
    }

    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER_GALLERY']
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)

        relative_path = os.path.relpath(image_path, 'static').replace("\\", "/")
        update_data["image"] = f"/static/{relative_path}"

    return update_data
