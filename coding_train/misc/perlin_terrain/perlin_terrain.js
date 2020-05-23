var cols, rows;
var scl = 20;
var w = 1200;
var h = 800;
var rand_vals;
var xoff, yoff;
var xoff_delta, yoff_delta;
var color_light_off;

function setup() {
	createCanvas(w , h, WEBGL);
  cols = w / scl;
  rows = h / scl;
  xoff_delta = 0.1;
  yoff_delta = 0.1;
  flight = 0.1;
  color_off = 0.1;
  color_light_off = 0;
  
  color1 = color(44, 4, 82) // purple
  color2 = color(255,113,206) // pink
}

function draw() {

	background(0);
  stroke(255);
  strokeWeight(1.5);
  noFill();
  setAttributes('antialias', true);
  
  rotateX(PI/3);
  //rotateY(PI/6);
  scale(2);
  translate(-w/2, -h/2, 0);
  //scale(1.5);

  yoff = flight;
  for (var y = 0; y <= rows; y++) {
    beginShape(TRIANGLE_STRIP);
    fill(lerpColor(color1, color2,
                   map(y, 0, rows/map(sin(color_light_off), 
                                      -1, 1 , 0.1, 5),
                       0, 1)));
    xoff = 0;
    for (var x = 0; x <= cols; x++) {

      //vertex(x*scl, y*scl, pr_hash(x,y));
      //vertex(x*scl, (y+1)*scl, pr_hash(x, y+1));
      v1_elev = map(
                    1    * noise(xoff,yoff) +
                    0.5  * noise(2*xoff,2*yoff) +
                    0.25 * noise(4*xoff,4*yoff), 
                    0, 1, -50, 50);
      v2_elev = map(
                    1    * noise(xoff,yoff + yoff_delta) +
                    0.5  * noise(2*xoff,2*(yoff + yoff_delta)) +
                    0.25 * noise(4*xoff,4*(yoff + yoff_delta)), 
                    0, 1, -50, 50);
      
      vertex(x*scl, y*scl, v1_elev); 
      vertex(x*scl, (y+1)*scl, v2_elev); 
      
      //vertex(x*scl, y*scl,
      //       map(noise(map(x, 0, cols, 0, cols/10),
      //                 map(y, 0, rows, 0, rows/10)),
      //           0, 1, -100, 100));
      //vertex(x*scl, (y+1)*scl,
      //       map(noise(map(x, 0, cols, 0, cols/10),
      //                 map(y+1, 0, rows, 0, rows/10)),
      //           0, 1, -100, 100));
      xoff += xoff_delta;
    }
    endShape();
    yoff += yoff_delta;  
  }
  flight -= 0.05;
  color_off += 1;
  color_light_off += 0.1;
}

function pr_hash(x,y){
 return perlin_vals[(x+y) % perlin_vals.length];
}
