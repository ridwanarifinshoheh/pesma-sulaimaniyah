from flask import Flask, render_template, request, redirect, session
from models import db, Santri
import os, uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/program")
def program():
    return render_template("program.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "POST":

        file = request.files.get("dokumen")
        filename = None

        if file:
            filename = str(uuid.uuid4()) + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = Santri.query.all()
    return render_template("admin.html", data=data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)