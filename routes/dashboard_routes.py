from flask import Blueprint, render_template, redirect
from config import db  # import koneksi MongoDB dari config.py

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin/dashboard")
def admin_dashboard():
    user_count = db["users"].count_documents({})
    batik_count = db["gallery"].count_documents({})
    article_count = db["articles"].count_documents({})
    event_count = db["events"].count_documents({})

    return render_template("dashboard.html",
        user_count=user_count,
        batik_count=batik_count,
        article_count=article_count,
        event_count=event_count
    )

@dashboard_bp.route("/")
def home():
    return redirect("/admin/dashboard")
