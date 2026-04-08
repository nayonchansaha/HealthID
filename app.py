from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import random
import string

app = Flask(__name__)

# Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
Session(app)

# Allowed file types for upload
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def get_db():
    """Connect to the SQLite database"""
    conn = sqlite3.connect("health.db")
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_health_id():
    """Generate a unique HealthID for each new user"""
    numbers = "".join(random.choices(string.digits, k=5))
    return f"HID-2026-{numbers}"

@app.route("/")
def index():
    """Homepage - show patient dashboard if logged in, otherwise show home page"""
    if "user_id" not in session:
        return render_template("home.html")
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    records = db.execute("SELECT * FROM records WHERE user_id = ? ORDER BY uploaded_at DESC", (session["user_id"],)).fetchall()
    db.close()
    return render_template("index.html", user=user, records=records)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new patient and assign a unique HealthID"""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        blood_group = request.form.get("blood_group")
        age = request.form.get("age")
        phone = request.form.get("phone")

        # Validate required fields
        if not name or not username or not password:
            return render_template("register.html", error="সব তথ্য দিন")

        # Generate unique HealthID and hash the password
        health_id = generate_health_id()
        hashed = generate_password_hash(password)

        try:
            db = get_db()
            db.execute("INSERT INTO users (health_id, name, username, password, blood_group, age, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (health_id, name, username, hashed, blood_group, age, phone))
            db.commit()
            db.close()
            return redirect("/login")
        except:
            # Username already exists in database
            return render_template("register.html", error="Username already exists")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing patient"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()

        # Verify username and password
        if user is None or not check_password_hash(user["password"], password):
            return render_template("login.html", error="Username বা Password ভুল")

        # Save user session
        session["user_id"] = user["id"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Clear session and log out the user"""
    session.clear()
    return redirect("/login")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload a new medical record (patients only)"""
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        file = request.files.get("file")

        if not title:
            return render_template("upload.html", error="Title দিন")

        # Save file if provided
        file_path = None
        if file and file.filename != "" and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Handle unnamed files
            if filename == "":
                filename = "file_" + "".join(random.choices(string.digits, k=6)) + "." + file.filename.rsplit(".", 1)[1].lower()
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            file_path = filename

        # Save record to database
        db = get_db()
        db.execute("INSERT INTO records (user_id, title, description, file_path) VALUES (?, ?, ?, ?)",
                   (session["user_id"], title, description, file_path))
        db.commit()
        db.close()
        return redirect("/")

    return render_template("upload.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    """Search patient records by HealthID (doctors/hospitals, no login required)"""
    user = None
    records = None
    error = None

    if request.method == "POST":
        health_id = request.form.get("health_id")
        if not health_id:
            error = "HealthID দিন"
        else:
            db = get_db()
            # Find patient by HealthID
            user = db.execute("SELECT * FROM users WHERE health_id = ?", (health_id,)).fetchone()
            if user:
                records = db.execute("SELECT * FROM records WHERE user_id = ? ORDER BY uploaded_at DESC", (user["id"],)).fetchall()
            else:
                error = "কোনো HealthID পাওয়া যায়নি"
            db.close()

    return render_template("search.html", user=user, records=records, error=error)

if __name__ == "__main__":
    app.run(debug=True)
