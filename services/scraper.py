import requests


def get_gempa():

    url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"

    response = requests.get(url)

    data = response.json()

    daftar_gempa = data["Infogempa"]["gempa"]

    hasil = []

    for gempa in daftar_gempa:

        hasil.append({

            "tanggal": gempa["Tanggal"],
            "jam": gempa["Jam"],
            "magnitude": gempa["Magnitude"],
            "kedalaman": gempa["Kedalaman"],
            "wilayah": gempa["Wilayah"],
            "potensi": gempa["Potensi"],
            "koordinat": gempa["Coordinates"]

        })

    return hasil