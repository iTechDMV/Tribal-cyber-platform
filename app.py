from flask import Flask, render_template, request, redirect
import os

# ------------------------------------------------------------
# Flask App Initialization
# ------------------------------------------------------------
app = Flask(__name__)

# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

@app.route("/")
def index():
    # Cinematic landing page
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: Add real authentication later
        return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: Add real registration logic later
        return redirect("/login")
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ------------------------------------------------------------
# Cloud Run Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    # Cloud Run requires listening on 0.0.0.0 and PORT env
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# ------------------------------------------------------------
# LANDING + AUTH
# ------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: Add authentication
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: Add registration logic
        return redirect("/login")
    return render_template("register.html")


# ------------------------------------------------------------
# PLATFORM PAGES
# ------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/assessments")
def assessments():
    return render_template("assessments.html")

@app.route("/governance")
def governance():
    return render_template("governance.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")


# ------------------------------------------------------------
# CLOUD RUN ENTRYPOINT
# ------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

