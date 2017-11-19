var time = 0.00;
var stopped = true;
var interval_timer = setInterval(my_timer, 10);

function my_timer() {
    if (stopped == false){
        time += 0.01;
    }
    document.getElementById("time").innerHTML = time.toFixed(2);
}

function init() {
    time = 0.00;
    document.getElementById("time").innerHTML = time;    

    //Add listener
    document.getElementById("start").onclick = start_stop;
    document.getElementById("reset").onclick = restart;
    document.getElementById("record").onclick = record;

    document.addEventListener("keydown", function(event) {
        if (event.key == "r") {
            restart();
        }
        else if (event.key == "s") {
            start_stop();
        }
        if (event.key == "t") {
            record();
        }
    });
}

function start_stop(){
    stopped = ! stopped;    
}

function restart() {
    time = 0.00;
    document.getElementById("time").innerHTML = time;

    clearInterval(interval_timer);
    interval_timer = setInterval(my_timer, 10);

    past = document.getElementById("past");

    while (past.firstChild) {
        past.removeChild(past.firstChild);
    }    
}

function record(){
    r = time.toFixed(2);
    document.getElementById("past").innerHTML += "<li>" + r + "</li>";    
}

init();

