var currentTime = new Date();

let dateObject = {
    fajrTime: [new Date("{{ time_to_js }} {{ times.fajr }}"), document.querySelectorAll(".fajr")],
    sunriseTime: [new Date("{{ time_to_js }} {{ times.sunrise }}"), document.querySelectorAll(".sunrise")],
    dhuhrTime: [new Date("{{ time_to_js }} {{ times.dhuhr }}"), document.querySelectorAll(".dhuhr")],
    asrTime: [new Date("{{ time_to_js }} {{ times.asr }}"), document.querySelectorAll(".asr")],
    maghribTime: [new Date("{{ time_to_js }} {{ times.maghrib }}"), document.querySelectorAll(".maghrib")],
    ishaTime: [new Date("{{ time_to_js }} {{ times.isha }}"), document.querySelectorAll(".isha")]
}

console.log(dateObject);

for (i in dateObject) {
    if (currentTime >= i[0]) {
        i[1].style.classList.add("bg-light")
    } else {
        i[1].style.classList.remove("bg-light")
    }
}

function changeStyleBasedOnTime(timeElement, timeValue) {
    if (currentTime >= timeValue) {
        timeElement.classList.add("bg-light");
    } else {
        timeElement.classList.remove("bg-light");
    }
}


// changeStyleBasedOnTime(document.getElementById("fajr"), fajrTime);
// changeStyleBasedOnTime(document.getElementById("sunrise"), sunriseTime);
// changeStyleBasedOnTime(document.getElementById("dhuhr"), dhuhrTime);
// changeStyleBasedOnTime(document.getElementById("asr"), asrTime);
// changeStyleBasedOnTime(document.getElementById("maghrib"), maghribTime);
// changeStyleBasedOnTime(document.getElementById("isha"), ishaTime);

