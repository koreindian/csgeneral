var grid = document.querySelectorAll("#grid td");
var time = 0;

var interval_timer = setInterval(my_timer, 1000);

var faceup_buffer = null;
var pairs_matched = 0;

function my_timer() {
    time += 1;
    var timer = document.getElementById("timer");
    timer.innerHTML = time;
}

function init() {
    time = 0;
    document.getElementById("timer").innerHTML = time;    
    setup_grid();

    //Add listener
    grid.forEach(function(cell) {
        cell.faceup = false;
        cell.solved = false;

        cell.addEventListener("mouseover", function() {
            if (cell.faceup == false && cell.solved == false) {
                cell.style.backgroundColor = "orange";
            }
        });
        
        cell.addEventListener("mouseout", function() {
            if (cell.faceup == false && cell.solved == false) {
                cell.style.backgroundColor = "blue";
            }
        });
        
        cell.addEventListener("mousedown", function() {
            if (cell.faceup == false) {
                flip_up(cell);
                if (faceup_buffer != null) {
                    if (cell.value == faceup_buffer.value) {
                        solve(cell);
                        solve(faceup_buffer);
                        pairs_matched += 1;
                        faceup_buffer = null;
                    }
                    else {
                        tmp = faceup_buffer;
                        faceup_buffer = null;
                        setTimeout( function(){
                            flip_down(cell);
                            flip_down(tmp);
                        }, 500);
                    }
                }
                else {
                    faceup_buffer = cell;
                }
            }
            if (pairs_matched == 4) {
                clearInterval(interval_timer);
                setTimeout(function() {
                    alert("You won in " + time + " seconds");
                }, 1);
            }
        });
    });

    document.addEventListener("keydown", function(event) {
        if (event.key === "r") {
            restart();
        }
    });

    document.getElementById("restart").onclick = restart;
}

function setup_grid() {
    var answers = [1,1,2,2,3,3,4,4,5]
    shuffle(answers);
    
    for (var i = 0; i < grid.length; i++) {
        grid[i].value = answers[i];
    }
}

function flip_up(cell) {
    cell.style.backgroundColor = "red";
    cell.innerHTML = cell.value;
    cell.faceup = true;
}

function flip_down(cell) {
    cell.style.backgroundColor = "blue";
    cell.innerHTML = "";
    cell.faceup = false;
}

function solve(cell) {
    cell.style.backgroundColor = "purple";
    cell.solved = true;
} 

//Knuth Shuffle
function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = arr[i];
        arr[i]  = arr[j];
        arr[j]  = tmp;
    } 
}

function restart() {
    time = 0;
    document.getElementById("timer").innerHTML = time;
    setup_grid();

    clearInterval(interval_timer);
    interval_timer = setInterval(my_timer, 1000);

    pairs_matched = 0;
    for (var i = 0; i < grid.length; i += 1){
        cell = grid[i];
        flip_down(cell);
        cell.solved = false;
    }
}

init();

