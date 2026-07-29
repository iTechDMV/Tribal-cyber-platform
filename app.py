#!/usr/bin/env python3
import os
import logging
from enum import Enum
from flask import Flask, request, jsonify

# Configure basic logging so warnings about APP_ENV are visible by default
logging.basicConfig(level=logging.INFO)

# Strict APP_ENV handling but allow a safe fallback with a warning
logger = logging.getLogger(__name__)

class AppEnv(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TEST = "test"

_raw_app_env = os.getenv("APP_ENV")
if _raw_app_env is None:
    # Missing -> warn and fall back to a safe local default
    logger.warning(
        "APP_ENV is not set. Falling back to %r for local/dev convenience. "
        "Set APP_ENV to one of: %s",
        AppEnv.DEVELOPMENT.value,
        [e.value for e in AppEnv],
    )
    APP_ENV = AppEnv.DEVELOPMENT.value
else:
    _app_env_normalized = _raw_app_env.strip().lower()
    if _app_env_normalized not in {e.value for e in AppEnv}:
        # Explicit but invalid -> fail fast so typos/misconfigurations are caught.
        raise RuntimeError(
            f"Invalid APP_ENV: {_raw_app_env!r}. Allowed values: {[e.value for e in AppEnv]}"
        )
    APP_ENV = _app_env_normalized

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
NTIA_MODE = os.environ.get("NTIA_MODE", "standard")
BIA_ENDPOINT = os.environ.get("BIA_ENDPOINT", "https://bia.gov/api")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["APP_ENV"] = APP_ENV
app.config["NTIA_MODE"] = NTIA_MODE
app.config["BIA_ENDPOINT"] = BIA_ENDPOINT

from src.federal.ntia_compliance import evaluate_ntia_controls
from src.federal.bia_integration import fetch_bia_requirements

@app.route("/healthz")
def healthz():
    return {"status": "ok", "service": "tribal-cyber-platform"}, 200

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/api/ntia/evaluate", methods=["POST"])
def ntia_evaluate():
    payload = request.json
    return jsonify(evaluate_ntia_controls(payload))

@app.route("/api/bia/requirements", methods=["GET"])
def bia_requirements():
    return jsonify(fetch_bia_requirements(app.config["BIA_ENDPOINT"]))

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

# Security headers middleware attached to the main app instance
@app.after_request
def apply_security_headers(response):
    response.headers["X-Tribal-Sovereignty"] = "Protected"
    response.headers["X-FIPS-Compliance"] = "AES-256-GCM"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cache-Control"] = "no-store"
    return response

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
