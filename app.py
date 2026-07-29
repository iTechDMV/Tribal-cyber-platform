#!/usr/bin/env python3
import os
import sqlite3
from flask import (
    Flask, render_template, request, jsonify, g
)

# ─────────────────────────────────────────────
# Flask App Configuration
# ─────────────────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "tribal_cyber.db")

# ─────────────────────────────────────────────
# Load NIST Families (moved out of app.py)
# ─────────────────────────────────────────────
from nist.families import NIST_FAMILIES

# ─────────────────────────────────────────────
# Database Helpers
# ─────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# ─────────────────────────────────────────────
# Routes — Frontend Pages
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", families=NIST_FAMILIES)

@app.route("/controls/<family_id>")
def controls(family_id):
    family = next((f for f in NIST_FAMILIES if f["id"] == family_id), None)
    if not family:
        return "Family not found", 404
    return render_template("controls.html", family=family)

# ─────────────────────────────────────────────
# API — NIST Families
# ─────────────────────────────────────────────
@app.route("/api/families")
def api_families():
    return jsonify(NIST_FAMILIES)

@app.route("/api/family/<family_id>")
def api_family(family_id):
    family = next((f for f in NIST_FAMILIES if f["id"] == family_id), None)
    if not family:
        return jsonify({"error": "Family not found"}), 404
    return jsonify(family)

# ─────────────────────────────────────────────
# API — Compliance Engine
# ─────────────────────────────────────────────
from compliance.engine import score_controls

@app.route("/api/score", methods=["POST"])
def api_score():
    data = request.json
    results = score_controls(data)
    return jsonify(results)

# ─────────────────────────────────────────────
# Local Dev Only — Cloud Run uses Gunicorn
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

