
var timer_running = false;
var start_time, end_time
var diff = 0;

var timer_display = document.getElementById("timer");
timer_display.innerHTML = diff;
document.body.addEventListener("keydown", keydown);
document.body.addEventListener("keyup", keyup);

function keyup() {
    timer_display.style.color = "#FFFFFF";

    start_time = new Date();
    timer_display.innerHTML = diff;
}

function keydown() {
    timer_display.style.color = "#33EE33";

    end_time = new Date();
    diff = (end_time - start_time) / 100;
    timer_display.innerHTML = diff;
}

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