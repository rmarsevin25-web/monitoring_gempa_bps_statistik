// ======================================
// LOADING SCREEN
// ======================================

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    setTimeout(function () {

        loader.style.opacity = "0";

        loader.style.visibility = "hidden";

    }, 800);

});

// ======================================
// TOAST
// ======================================

function showToast(message, warna = "success") {

    const toast = document.getElementById("liveToast");

    toast.className =
        "toast align-items-center text-bg-" +
        warna +
        " border-0";

    document.getElementById("toastMessage").innerHTML = message;

    const bsToast = new bootstrap.Toast(toast);

    bsToast.show();

}

window.addEventListener("load",function(){

    setTimeout(function(){

        showToast("✅ Selamat Datang di GeoQuake Indonesia");

    },1200);

});

// ======================================
// COUNTER ANIMATION
// ======================================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const target = parseFloat(counter.dataset.target);

    const isDecimal = target % 1 !== 0;

    let current = 0;

    const step = target / 80;

    function updateCounter(){

        current += step;

        if(current >= target){

            counter.innerHTML = isDecimal
                ? target.toFixed(2)
                : Math.round(target);

            return;

        }

        counter.innerHTML = isDecimal
            ? current.toFixed(2)
            : Math.round(current);

        requestAnimationFrame(updateCounter);

    }

    updateCounter();

});

// ======================================
// DARK MODE
// ======================================

const darkBtn = document.getElementById("darkModeBtn");

if(localStorage.getItem("theme") === "dark"){

    document.body.classList.add("dark-mode");

    darkBtn.innerHTML = "☀ Light";

}

darkBtn.addEventListener("click",function(){

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){

        localStorage.setItem("theme","dark");

        darkBtn.innerHTML="☀ Light";

    }else{

        localStorage.setItem("theme","light");

        darkBtn.innerHTML="🌙 Dark";

    }

});