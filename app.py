import os
import uuid
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from models import db, Santri

app = Flask(__name__)

# CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

db.init_app(app)

# INIT DATABASE
with app.app_context():
    db.create_all()

# FUNCTION CEK FILE
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# DAFTAR + UPLOAD FILE
@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "POST":
        file = request.files.get("dokumen")
        filename = None

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        data = Santri(
            nama=request.form["nama"],
            email=request.form["email"],
            no_hp=request.form["no_hp"],
            dokumen=filename
        )

        db.session.add(data)
        db.session.commit()

        return redirect("/")

    return render_template("daftar.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

# ADMIN
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = Santri.query.all()
    return render_template("admin.html", data=data)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)