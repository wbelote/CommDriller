
var timer_running = false;
var start_time, end_time;
var diff = 0.0;

var timer_display = document.getElementById("time-display");
var timer_entry = document.getElementById("time-entry");
timer_display.innerHTML = "ready";

document.addEventListener("keydown", (event) => {

    if (timer_running) {
        end_time = new Date();
        diff = (end_time - start_time) / 1000;
        timer_display.innerHTML = diff;
        timer_entry.value = diff;
        timer_running = false;
    } else if (event.code == "Space") {
        timer_display.style.color = "#33EE33";
        diff = 0.0;
        timer_display.innerHTML = diff;
    }

    timer_entry.value = timer_entry.value.trim();

});

document.addEventListener("keyup", (event) => {

    timer_display.style.color = "#FFFFFF";

    if (diff < 0.1) {
        start_time = new Date();
        timer_running = true;
        timer_display.innerHTML = diff;
    }

    if (event.code == "Space") {
        timer_entry.value = timer_entry.value.trim();
    }

});

timer_entry.addEventListener("onchange", function (event) {
})

/*

var timer_running = false;
var start_time, end_time, diff;

var timer_display = document.getElementById("timer");
timer_display.innerHTML = "script";
document.body.addEventListener("keydown", timer_stop);
document.body.addEventListener("keyup", timer_start);

function timer_start() {
    timer_display.color = "#33EE33";
    if (!timer_running) {
        start_time = new Date();
        timer_display.innerHTML = "0.00";
    } else {
        timer_display.innerHTML = diff;
    }
}

function timer_stop() {
    timer_display.color = "#FFFFFF";
    if (timer_running) {
        end_time = new Date();
        diff = end_time - start_time;
        timer_display.innerHTML = diff;
    }
}
*/