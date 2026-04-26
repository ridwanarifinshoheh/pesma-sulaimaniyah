from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Santri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    no_hp = db.Column(db.String(20))
    dokumen = db.Column(db.String(200))  # path file