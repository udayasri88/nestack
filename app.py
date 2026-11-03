from flask import Flask, send_from_directory

from routes.auth import auth_bp
from routes.records import records_bp

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path="/frontend"
)

# Register API routes
app.register_blueprint(auth_bp)
app.register_blueprint(records_bp)


# Registration page
@app.route("/register-page")
def register_page():
    return send_from_directory("frontend", "register.html")


# Login page
@app.route("/login-page")
def login_page():
    return send_from_directory("frontend", "login.html")


# Home page
@app.route("/")
def home():
    return send_from_directory("frontend", "login.html")

@app.route("/dashboard-page")
def dashboard_page():
    return send_from_directory("frontend", "dashboard.html")

if __name__ == "__main__":
    app.run(debug=False, port=5000)