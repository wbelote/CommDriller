
var timer_running = false;
var start_time, end_time;
var diff = 0.0;

var timer_display = document.getElementById("time-display");
var timer_entry = document.getElementById("time-entry");
timer_display.innerHTML = "ready";

document.addEventListener("keyup", function (event) {
    timer_display.style.color = "#FFFFFF";

    if (diff < 0.1) {
        start_time = new Date();
        timer_running = true;
        timer_display.innerHTML = diff;
    }
});

document.addEventListener("keydown", function (event) {
    timer_display.style.color = "#33EE33";
    if (timer_running) {
        end_time = new Date();
        diff = (end_time - start_time) / 1000;
        timer_display.innerHTML = diff;
        timer_entry.value = diff;
    }
    timer_running = false;
});

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