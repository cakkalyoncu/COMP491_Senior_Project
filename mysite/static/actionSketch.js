let obj;
let actions;
let time;
let speed;

function setup(){
    let arr = [[[70,60,39,14,2,1,14,57,60,56,56,59,70,105,128,139,141],[3,0,1,15,34,64,79,86,90,113,147,157,175,203,211,211,208]],[[72,79,155,174,178,174,169,140,124],[0,5,110,150,189,195,198,199,204]],[[127,111,110,115,132,143,176,231],[74,106,135,149,176,185,188,174]],[[128,131,143,194,225,252,255,249,224],[66,78,89,127,146,168,173,176,176]],[[92,92,96],[206,237,253]],[[136,147],[193,244]],[[106,73],[251,249]],[[149,113],[244,248]]];
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