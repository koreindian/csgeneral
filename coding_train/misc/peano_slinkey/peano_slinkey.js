// Reference: https://twitter.com/beesandbombs/status/1181004514364657664?s=20
var num_circles = 12; 
var y_range = 200;
var radius = 160;
var circle_pos_l = [];
var wave_angle = 0;

function setup() {
    createCanvas(500, 500);
    angleMode(RADIANS);

    for (let i = 0; i < num_circles; i++) {
        console.log(i, 0, num_circles, -y_range/2, y_range/2);
        console.log(map(i, 0, num_circles, -y_range/2, y_range/2));
        let pos_dict = {
          "x": 0, 
          "y": map(i, 0, num_circles, -y_range/2, y_range/2)
        };
        circle_pos_l.push(pos_dict); 

    }
    console.log(circle_pos_l);
}

function draw() {
    background(0);
    translate(width/2, height/2);
    noFill();
    strokeWeight(2);
    
    let num_arcs = 36;

    for (let i = 0; i < num_circles; i++) {
      let arc_size = map(i, 0, num_circles,
                         TWO_PI / num_arcs, 0); 
      circle_alpha = map(i, 0, num_circles, 255, 255/2);
      stroke(255,255,255, circle_alpha);
      for (let j = 0; j < num_arcs; j++) {
        beginShape();
        arc_start = map(j, 0, num_arcs, 0, TWO_PI);
        arc(circle_pos_l[i].x,
            circle_pos_l[i].y,
            radius, radius, arc_start, arc_start + arc_size);
        endShape(CLOSE);
      }
      let offset = map(i,
                       0,
                       num_circles,
                       0, PI);
      let new_y = map(sin(wave_angle - offset),
                      -1, 1, - y_range/2, y_range/2);
      circle_pos_l[i].y = new_y;
    }

    wave_angle += PI / 120;
}
