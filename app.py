# =========================
# IMPORT
# =========================
import os
import uuid
import requests

from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from models import db, Santri


# =========================
# INIT APP
# =========================
app = Flask(__name__)

# Config utama
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# File yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

from sqlalchemy import text

# Init database
db.init_app(app)

# Buat database jika belum ada dan pastikan kolom dokumen ada
with app.app_context():
    db.create_all()
    try:
        result = db.session.execute(text("PRAGMA table_info('santri')")).mappings().all()
        columns = [row['name'] for row in result]
        if 'dokumen' not in columns:
            db.session.execute(text("ALTER TABLE santri ADD COLUMN dokumen VARCHAR(200)"))
            db.session.commit()
    except Exception:
        db.session.rollback()


# =========================
# HELPER FUNCTION
# =========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# ROUTES
# =========================

# 🏠 HOME
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def kontak():
    return render_template("contact.html")

# 📋 DAFTAR SANTRI + UPLOAD + GOOGLE SHEETS
@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "POST":

        # =========================
        # 1. HANDLE UPLOAD FILE
        # =========================
        file = request.files.get("dokumen")
        filename = None

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        # =========================
        # 2. SIMPAN KE DATABASE
        # =========================
        data = Santri(
            nama=request.form["nama"],
            email=request.form["email"],
            no_hp=request.form["no_hp"],
            dokumen=filename
        )

        db.session.add(data)
        db.session.commit()

        # =========================
        # 3. KIRIM KE GOOGLE SHEETS
        # =========================
        try:
            url = "https://script.google.com/macros/s/AKfycbwJYBopzQ0Vk4xJoxDWNmJkaKiJ_FQifnGOokBHF_U/exec"

            data_sheet = {
                "nama": request.form["nama"],
                "email": request.form["email"],
                "no_hp": request.form["no_hp"],
                "dokumen": filename
            }

            response = requests.post(url, json=data_sheet, timeout=5)

            if response.status_code != 200:
                print("Gagal kirim:", response.text)

        except Exception as e:
            print("ERROR GOOGLE SHEETS:", e)
            print(data_sheet)

        return redirect("/")

    return render_template("daftar.html")


# 🔐 LOGIN ADMIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")


# 📊 DASHBOARD ADMIN
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = Santri.query.all()
    return render_template("admin.html", data=data)


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)