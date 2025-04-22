# app/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.policy_data import policy_data

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if request.method == "POST":
        new_policy = {
            "name": request.form["name"],
            "description": request.form["description"],
            "link": request.form["link"],
            "category": request.form["category"]
        }
        policy_data.append(new_policy)
        return redirect(url_for("admin.admin_panel"))
    return render_template("admin.html", policies=policy_data)
