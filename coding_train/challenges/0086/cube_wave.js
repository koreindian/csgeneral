let angle = 0;
let box_w = 30;
let num_boxes = 16;
let canvas_w = box_w * num_boxes;
let canvas_h = box_w * num_boxes;
let magicangle;
let maxD;

function setup() {
    createCanvas(canvas_w, canvas_h, WEBGL);
    magicangle = atan(1 / sqrt(2));
    maxD = dist(0, 0, canvas_w / 2, canvas_h / 2);
}

function draw() {
    background(255);
    ortho(-400, 400, -400, 400, 0, 1000);

    strokeWeight(0);

    rotateX(-magicangle);
    rotateY(-QUARTER_PI);

    let offset = 0;
    for (let z = 0; z < height; z += box_w) {
        for (let x = 0; x < width; x += box_w) {
            push();
            let d = dist(x, z, width / 2, height / 2);
            let offset = map(d, 0, maxD, 0, 2 * PI);

            let theta = angle + offset;
            let h = floor(map(sin(theta), -1, 1, 100, canvas_h)); 
            normalMaterial();
            translate(x - width / 2, 0, z - height / 2);
            box(box_w, h, box_w);
            pop();
        }
        offset += 2 * PI / num_boxes;
    }
    angle -= PI / 60;
}
