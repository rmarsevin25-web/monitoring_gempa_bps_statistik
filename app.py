from io import BytesIO
from flask import send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)
from models import db, Gempa
from services.scraper import get_gempa
from models import Gempa, StatistikBPS, Admin
import pandas as pd
from flask import request
from models import Admin
from openpyxl import Workbook
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = "geoquake123"

# ==========================
# KONFIGURASI DATABASE
# ==========================
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/bps_lubuklinggau"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ==========================
# DASHBOARD
# ==========================
@app.route("/")
def home():

    semua_data = Gempa.query.order_by(Gempa.id.desc()).all()

    total_data = len(semua_data)

    magnitude_terbesar = 0

    if semua_data:
        magnitude_terbesar = max(
            float(item.magnitude)
            for item in semua_data
        )

    # ==========================
    # DATA BPS
    # ==========================

    bps = StatistikBPS.query.all()

    total_provinsi = len(bps)

    if total_provinsi > 0:

        rata_kepadatan = round(
            sum(item.kepadatan for item in bps) / total_provinsi,
            2
        )

        provinsi_terpadat = max(
            bps,
            key=lambda x: x.kepadatan
        )

    else:

        rata_kepadatan = 0
        provinsi_terpadat = None

    return render_template(
        "index.html",
        data=semua_data,
        total_data=total_data,
        magnitude_terbesar=magnitude_terbesar,
        terbaru=semua_data[0] if semua_data else None,
        bps=bps,
        total_provinsi=total_provinsi,
        rata_kepadatan=rata_kepadatan,
        provinsi_terpadat=provinsi_terpadat
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session["admin"] = admin.username

            flash("Login berhasil!")

            return redirect(url_for("home"))

        else:

            flash("Username atau Password salah!")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    flash("Logout berhasil")

    return redirect(url_for("login"))


# ==========================
# UPDATE DATA DARI BMKG
# ==========================
@app.route("/update")
def update_data():
    if "admin" not in session:

        return redirect(url_for("login"))

    daftar_gempa = get_gempa()

    for data in daftar_gempa:

        cek = Gempa.query.filter_by(
            tanggal=data["tanggal"],
            jam=data["jam"]
        ).first()

        if not cek:

            gempa = Gempa(
                tanggal=data["tanggal"],
                jam=data["jam"],
                magnitude=data["magnitude"],
                kedalaman=data["kedalaman"],
                wilayah=data["wilayah"],
                potensi=data["potensi"],
                koordinat=data["koordinat"]
            )

            db.session.add(gempa)

    db.session.commit()

    return redirect(url_for("home"))
# ==========================
# HAPUS DATA GEMPA
# ==========================
@app.route("/delete/<int:id>")
def delete_data(id):
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = Gempa.query.get_or_404(id)

    db.session.delete(data)
    db.session.commit()

    return redirect(url_for("home"))

# ==========================
# EDIT DATA GEMPA
# ==========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_data(id):
    if "admin" not in session:
    
            return redirect(url_for("login"))

    gempa = Gempa.query.get_or_404(id)

    if request.method == "POST":

        gempa.tanggal = request.form["tanggal"]
        gempa.jam = request.form["jam"]
        gempa.magnitude = request.form["magnitude"]
        gempa.kedalaman = request.form["kedalaman"]
        gempa.wilayah = request.form["wilayah"]
        gempa.potensi = request.form["potensi"]
        gempa.koordinat = request.form["koordinat"]

        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "edit.html",
        gempa=gempa
    )

# ==========================
# HALAMAN RIWAYAT
# ==========================
@app.route("/history")
def history():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = Gempa.query.order_by(Gempa.id.desc()).all()

    return render_template(
        "dashboard.html",
        data=data
    )


# ==========================
# HALAMAN TENTANG
# ==========================
@app.route("/chart-data")
def chart_data():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = Gempa.query.order_by(Gempa.id.asc()).all()

    hasil = []

    for item in data:
        hasil.append({
            "tanggal": item.tanggal,
            "magnitude": float(item.magnitude)
        })

    return jsonify(hasil)

@app.route("/chart-bps")
def chart_bps():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = StatistikBPS.query.order_by(StatistikBPS.kepadatan.desc()).all()

    hasil = []

    for item in data:

        hasil.append({
            "provinsi": item.provinsi,
            "kepadatan": item.kepadatan
        })

    return jsonify(hasil)

@app.route("/map-data")
def map_data():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = Gempa.query.all()

    hasil = []

    for item in data:

        hasil.append({
            "tanggal": item.tanggal,
            "jam": item.jam,
            "wilayah": item.wilayah,
            "magnitude": item.magnitude,
            "kedalaman": item.kedalaman,
            "potensi": item.potensi,
            "koordinat": item.koordinat
        })

    return jsonify(hasil)

@app.route("/statistik")
def statistik():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    data = Gempa.query.order_by(Gempa.id.desc()).all()

    total_data = len(data)

    if total_data == 0:
        return render_template(
            "statistik.html",
            total_data=0,
            rata_rata=0,
            terbesar=0,
            terkecil=0
        )

    magnitudes = [float(item.magnitude) for item in data]

    rata_rata = round(sum(magnitudes) / len(magnitudes), 2)
    terbesar = max(magnitudes)
    terkecil = min(magnitudes)

    return render_template(
        "statistik.html",
        total_data=total_data,
        rata_rata=rata_rata,
        terbesar=terbesar,
        terkecil=terkecil
    )
@app.route("/analisis")
def analisis():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    total_gempa = Gempa.query.count()

    rata_magnitude = db.session.query(db.func.avg(Gempa.magnitude)).scalar()

    if rata_magnitude:
        rata_magnitude = round(rata_magnitude, 2)
    else:
        rata_magnitude = 0

    total_provinsi = StatistikBPS.query.count()

    rata_kepadatan = db.session.query(
        db.func.avg(StatistikBPS.kepadatan)
    ).scalar()

    if rata_kepadatan:
        rata_kepadatan = round(rata_kepadatan, 2)
    else:
        rata_kepadatan = 0

    bps = StatistikBPS.query.order_by(
        StatistikBPS.kepadatan.desc()
    ).limit(10).all()

    return render_template(
        "analisis.html",
        total_gempa=total_gempa,
        rata_magnitude=rata_magnitude,
        total_provinsi=total_provinsi,
        rata_kepadatan=rata_kepadatan,
        bps=bps
    )

@app.route("/export/pdf")
def export_pdf():
    if "admin" not in session:

        return redirect(url_for("login"))

    data = Gempa.query.order_by(Gempa.id.desc()).all()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)

    rows = []

    rows.append([
        "No",
        "Tanggal",
        "Jam",
        "Mag",
        "Kedalaman",
        "Wilayah"
    ])

    for i, item in enumerate(data, start=1):

        rows.append([
            i,
            item.tanggal,
            item.jam,
            item.magnitude,
            item.kedalaman,
            item.wilayah
        ])

    table = Table(rows)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

    ]))

    doc.build([table])

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="laporan_gempa.pdf",
        mimetype="application/pdf"
    )

@app.route("/export/excel")
def export_excel():

    # Proteksi Login
    if "admin" not in session:
        return redirect(url_for("login"))

    data = Gempa.query.all()

    wb = Workbook()

    ws = wb.active

    ws.title = "Data Gempa"

    # Header
    ws.append([
        "No",
        "Tanggal",
        "Jam",
        "Magnitude",
        "Kedalaman",
        "Wilayah",
        "Potensi"
    ])

    # Isi Data
    for i, item in enumerate(data, start=1):

        ws.append([
            i,
            item.tanggal,
            item.jam,
            item.magnitude,
            item.kedalaman,
            item.wilayah,
            item.potensi
        ])

    output = io.BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(

        output,

        download_name="Data_Gempa.xlsx",

        as_attachment=True,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

@app.route("/import-bps", methods=["GET", "POST"])
def import_bps():
    if "admin" not in session:
    
            return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files["file"]

        df = pd.read_csv(file)

        # Ambil dua kolom pertama
        df = df.iloc[:, :2]

        # Ganti nama kolom
        df.columns = ["provinsi", "kepadatan"]

        # Hapus baris kosong
        df = df.dropna()

        # Hapus data lama
        StatistikBPS.query.delete()

        for _, row in df.iterrows():

            try:
                kepadatan = float(row["kepadatan"])
            except:
                continue

            data = StatistikBPS(
                provinsi=row["provinsi"],
                kepadatan=kepadatan
            )

            db.session.add(data)

        db.session.commit()

        return "Import Berhasil!"

    return render_template("import_bps.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# MENJALANKAN FLASK
# ==========================
if __name__ == "__main__":
    app.run(debug=True)