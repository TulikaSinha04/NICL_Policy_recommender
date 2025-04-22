# app/routes.py

from flask import Blueprint, render_template, request
from app.model import get_best_policies
from app.policy_data import policy_data
from collections import defaultdict

bp = Blueprint('main', __name__)

# Global dictionary to store keyword counts
search_counts = defaultdict(int)

@bp.route("/", methods=["GET", "POST"])
def index():
    results = {
        "best_matches": [],
        "suggestions": [],
        "no_matches": False
    }
    top_keywords = []

    if request.method == "POST":
        keywords = request.form.get("keywords", "").strip()
        selected_categories = request.form.getlist("categories")

        if keywords:
            search_counts[keywords.lower()] += 1  # Track keyword usage

        # Filter policies by selected category
        filtered_data = [p for p in policy_data if p["category"] in selected_categories] if selected_categories else policy_data

        results = get_best_policies(keywords, filtered_data)

    # Get top 5 keywords
    sorted_keywords = sorted(search_counts.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, _ in sorted_keywords[:5]]

    return render_template("index.html", results=results, top_keywords=top_keywords)
