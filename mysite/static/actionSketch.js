let obj;
let actions;
let time;
let speed;

function setup(){
    let arr = [[[220, 199, 189, 179, 160, 146, 143, 148, 156, 168, 183, 197, 209, 217, 223, 225, 223, 218, 209, 187], [87, 75, 72, 76, 98, 131, 162, 174, 181, 184, 182, 176, 166, 152, 136, 121, 108, 100, 92, 83]], [[148, 138, 128, 100, 67, 43, 32, 26, 28, 37, 62, 147], [117, 106, 102, 96, 95, 104, 112, 123, 137, 149, 165, 180]], [[28, 0, 43, 1], [115, 108, 116, 113]], [[94, 91, 94, 99, 107, 114, 121, 130, 137, 143], [83, 46, 15, 6, 1, 0, 7, 22, 50, 130]], [[83, 82, 88, 90, 103, 108, 124, 128, 127, 115], [169, 207, 242, 248, 255, 253, 219, 204, 187, 166]]];
    var canvas = createCanvas(1050,450);
    canvas.parent("sketch");
    actions = JSON.parse(document.getElementById('actions').textContent);
//    alert(actions);
    obj = new DrawingObject("bird", 0, 1, 1, 420, 170, arr);
    time = 0;
    speed = true;
    frameRate(20);
}
function draw(){
    background(color(135,206,250));
    ground(color(0,255,0));
    obj.display();
    if(actions[time % actions.length] == "fly"){
        obj.fly();
    } else if(actions[time % actions.length] == "ascend"){
        obj.ascend();
    } else if(actions[time % actions.length] == "goRight"){
        obj.goRight();
    } else if(actions[time % actions.length] == "goLeft"){
        obj.goLeft();
    }
    if(speed){
        time +=1;
        speed = false;
    } else {
        speed = true;
    }
}

function ground(color){
    stroke(0);
    fill(color);
    strokeWeight(1);
    beginShape();
    vertex(0,410);
   curveVertex(0,410);
    curveVertex(530,370);
    curveVertex(1060,410);
    vertex(1060,455);
    curveVertex(0,455);
    vertex(0,410);
    endShape();
}