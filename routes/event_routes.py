from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bson import ObjectId
from datetime import datetime
from pytz import timezone
from dateutil import tz  # ✅ Tambahkan ini
import os
from config import event_col

event_bp = Blueprint("event_web", __name__)

# Halaman Index Event
@event_bp.route("/admin/event")
def event_index():
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    events = list(event_col.find())
    return render_template("event/index.html", events=events)

# buat event

@event_bp.route("/admin/event/create", methods=["GET", "POST"])
def create_event():
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    if request.method == "POST":
        judul = request.form.get("judul")
        waktu_str = request.form.get("datetime")
        lokasi = request.form.get("lokasi")
        deskripsi = request.form.get("deskripsi")
        foto = request.files.get("foto")

        # Parsing waktu ke WIB (zona Asia/Jakarta)
        waktu = datetime.strptime(waktu_str, "%Y-%m-%dT%H:%M")
        waktu = waktu.replace(tzinfo=tz.tzlocal())
        waktu = waktu.astimezone(timezone("Asia/Jakarta"))

        filename = ""
        if foto:
            filename = foto.filename
            path = os.path.join("static/uploads", filename)
            foto.save(path)

        event_col.insert_one({
            "judul": judul,
            "datetime": waktu,
            "lokasi": lokasi,
            "deskripsi": deskripsi,
            "foto": filename
        })

        flash("Event berhasil ditambahkan!", "success")
        return redirect(url_for("event_web.event_index"))

    return render_template("event/create.html")

#Edit Event
@event_bp.route("/admin/event/edit/<id>", methods=["GET", "POST"])
def edit_event(id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    event = event_col.find_one({"_id": ObjectId(id)})
    if not event:
        return "Event tidak ditemukan", 404

    if request.method == "POST":
        judul = request.form.get("judul")
        waktu_str = request.form.get("datetime")
        lokasi = request.form.get("lokasi")
        deskripsi = request.form.get("deskripsi")
        foto = request.files.get("foto")

        # Parsing waktu ke WIB
        waktu = datetime.strptime(waktu_str, "%Y-%m-%dT%H:%M")
        waktu = waktu.replace(tzinfo=tz.tzlocal())
        waktu = waktu.astimezone(timezone("Asia/Jakarta"))

        update_data = {
            "judul": judul,
            "datetime": waktu,
            "lokasi": lokasi,
            "deskripsi": deskripsi
        }

        if foto:
            filename = foto.filename
            path = os.path.join("static/uploads", filename)
            foto.save(path)
            update_data["foto"] = filename

        event_col.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        flash("Event berhasil diperbarui!", "success")
        return redirect(url_for("event_web.event_index"))

    return render_template("event/edit.html", event=event)



# Hapus Event
@event_bp.route("/admin/event/delete/<id>")
def delete_event(id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    event_col.delete_one({"_id": ObjectId(id)})
    flash("Event berhasil dihapus!", "info")
    return redirect(url_for("event_web.event_index"))
