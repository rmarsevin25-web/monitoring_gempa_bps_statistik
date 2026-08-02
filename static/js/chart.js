/* ==========================================================
   CHART MAGNITUDE GEMPA
========================================================== */

const chartGempa = document.getElementById("chartGempa");

if (chartGempa) {

    fetch("/chart-data")
        .then(res => res.json())
        .then(data => {

            const labels = data.map(item => item.tanggal);
            const magnitudes = data.map(item => item.magnitude);

            new Chart(chartGempa, {

                type: "line",

                data: {

                    labels: labels,

                    datasets: [{

                        label: "Magnitude Gempa",

                        data: magnitudes,

                        borderColor: "#dc3545",

                        backgroundColor: "rgba(220,53,69,.15)",

                        fill: true,

                        tension: .35

                    }]

                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {

                            display: true

                        }

                    }

                }

            });

        });

}


/* ==========================================================
   CHART BPS
========================================================== */

const chartBPS = document.getElementById("chartBPS");

if (chartBPS) {

    fetch("/chart-bps")

        .then(res => res.json())

        .then(data => {

            const labels = data.map(item => item.provinsi);

            const values = data.map(item => item.kepadatan);

            new Chart(chartBPS, {

                type: "bar",

                data: {

                    labels: labels,

                    datasets: [{

                        label: "Kepadatan Penduduk",

                        data: values,

                        backgroundColor: "rgba(54,162,235,.75)"

                    }]

                },

                options: {

                    responsive: true,

                    indexAxis: "y",

                    plugins: {

                        legend: {

                            display: false

                        }

                    }

                }

            });

        });

}


/* ==========================================================
   SEARCH TABEL
========================================================== */

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const keyword = this.value.toLowerCase();

        const rows = document.querySelectorAll("#gempaTable tr");

        rows.forEach(row => {

            row.style.display = row.innerText
                .toLowerCase()
                .includes(keyword)
                ? ""
                : "none";

        });

    });

}


/* ==========================================================
   PETA LEAFLET
========================================================== */

const mapElement = document.getElementById("map");

if (mapElement) {

    const map = L.map("map").setView([-2.5,118],5);

    L.tileLayer(

        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

        {

            attribution: "&copy; OpenStreetMap"

        }

    ).addTo(map);


    fetch("/map-data")

        .then(res => res.json())

        .then(data => {

            data.forEach(gempa => {

                if (!gempa.koordinat) return;

                const koordinat = gempa.koordinat.split(",");

                const latitude = parseFloat(koordinat[0]);

                const longitude = parseFloat(koordinat[1]);

                if (isNaN(latitude) || isNaN(longitude)) return;


                /* =====================================
                   WARNA MARKER
                ===================================== */

                let warna = "green";

                if (gempa.magnitude >= 6){

                    warna = "red";

                }

                else if (gempa.magnitude >= 5){

                    warna = "orange";

                }

                else if (gempa.magnitude >= 4){

                    warna = "yellow";

                }


                L.circleMarker(

                    [latitude, longitude],

                    {

                        radius:8,

                        color:warna,

                        fillColor:warna,

                        fillOpacity:.85,

                        weight:2

                    }

                )

                .addTo(map)

                .bindPopup(`

                    <b>🌍 ${gempa.wilayah}</b><br>

                    <b>Magnitude :</b> ${gempa.magnitude}<br>

                    <b>Kedalaman :</b> ${gempa.kedalaman}<br>

                    <b>Tanggal :</b> ${gempa.tanggal}<br>

                    <b>Potensi :</b> ${gempa.potensi}

                `);

            });

        });

}