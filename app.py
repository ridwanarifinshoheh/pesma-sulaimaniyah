from flask import Flask, render_template, request, redirect
from models import db, Santri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "POST":
        data = Santri(
            nama=request.form["nama"],
            email=request.form["email"],
            no_hp=request.form["no_hp"]
        )
        db.session.add(data)
        db.session.commit()
        return redirect("/")

    return render_template("daftar.html")

from flask import session

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = Santri.query.all()
    return render_template("admin.html", data=data)