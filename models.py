from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gempa(db.Model):
    __tablename__ = "gempa"

    id = db.Column(db.Integer, primary_key=True)

    tanggal = db.Column(db.String(50), nullable=False)
    jam = db.Column(db.String(30), nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    kedalaman = db.Column(db.String(30))
    wilayah = db.Column(db.String(200), nullable=False)
    potensi = db.Column(db.String(200))
    koordinat = db.Column(db.String(100))

    def __repr__(self):
        return f"<Gempa {self.wilayah}>"


class StatistikBPS(db.Model):
    __tablename__ = "statistik_bps"

    id = db.Column(db.Integer, primary_key=True)
    provinsi = db.Column(db.String(100), nullable=False)
    kepadatan = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<StatistikBPS {self.provinsi}>"

    # ==========================================
# TABEL ADMIN
# ==========================================

class Admin(db.Model):

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):

        return f"<Admin {self.username}>"