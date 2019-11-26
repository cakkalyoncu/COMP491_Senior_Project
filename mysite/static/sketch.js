let obj_array = [];
let pause = false;
let sky_blue;
let snowflakes = [];
let raindrops = [];
let snow = false;
let rain = false;


function randomIntFromInterval(min, max) { // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function findObject(relativeTo){
    for (let i = 0 ; i < obj_array.length; i++){
        if(obj_array[i].name == relativeTo){
            return obj_array[i];
        }
    }
    return obj_array[0];
}

function getLocation(json_obj){
    let loc = json_obj.location;
    // alert(json_obj.location);
    if(loc == "random"){
        let x = randomIntFromInterval(300,400);
        let y;
        if(json_obj.action == null || json_obj.action == undefined || json_obj.action =="walking"){
//alert("here");
//alert(json_obj.action);
            y = randomIntFromInterval(300,350);
            if(json_obj.size ==1.5){
                y = randomIntFromInterval(160,180);
            }
        }else{
      //      alert(json_obj.action);
            y = randomIntFromInterval(100,130);
        }

        //  alert (  "x: "+ x + " y: "+ y);
        //    alert(y);
        return [x,y];
    }
    // Has a specified position
    else{
        let prep = loc.Preposition;
        let relativeTo = loc.Location;
        let relativeObject = findObject(relativeTo);
        if(prep == "on"){
            let x = randomIntFromInterval(relativeObject.location_X-10,relativeObject.location_X+10);
            let y = randomIntFromInterval(relativeObject.location_Y-50,relativeObject.location_Y-150);
            //   alert("on  rx: "+relativeObject.location_X + " ry: "+ relativeObject.location_Y  +" x: "+ x + " y: "+ y);
            return[x,y];

        }
        else if(prep == "under"){
            let x =randomIntFromInterval(relativeObject.location_X-10,relativeObject.location_X+10);
            let y = randomIntFromInterval(relativeObject.location_Y+150,relativeObject.location_Y+200);
            //   alert("under  rx: "+relativeObject.location_X + " ry: "+ relativeObject.location_Y  +" x: "+ x + " y: "+ y);
            return[x,y];

        }
        else{
            return [randomIntFromInterval(200,300),
                randomIntFromInterval(90,110)];
        }
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

let width = 1060;
let height = 450;

function setup() {

    prepareRain();
    sky_blue = color(135,206,250);
    let list = JSON.parse(document.getElementById('json').textContent);
//   alert(list);
    let err = JSON.parse(document.getElementById('error').textContent);
    if(err!=""){
        alert(err);
    }
    let weather = JSON.parse(document.getElementById('weather').textContent);
    if(weather!=""){
        if(weather=="snow"){
            snow = true;
            rain = false;
        } else if(weather=="rain"){
            snow = false;
            rain = true;
        } else if(weather=="sun"){
            snow = false;
            rain = false;
        }
    }
    for (let i = 0; i< list.length; i++){
        let a = JSON.parse(list[i]);
        //alert(a.name)

        //alert(w);
        //alert(h);
        let location = getLocation(a);
        for(let m =0; m< a.number; m++){

            let w = location[0]+ (m * 120);
            let h = location[1];
        //    alert(a.name+" : "+ a.number+ " w: "+w);
            let obj = new DrawingObject(a.name, a.color, a.size, a.number, w, h, a.strokeArray, a.action);
            obj_array.push(obj);
        }

        time =0;
    }

    var canvas = createCanvas(width,height);
    canvas.parent("sketchholder");
    frameRate(20);
}

function letItSnow(){
    background(sky_blue);
    ground(255);
    for (let i = 0; i < random(5); i++) {
        snowflakes.push(new snowflake());
    }
    for (let flake of snowflakes) {
        flake.update(frameCount / 60);
        flake.display();
    }
}
function prepareRain(){
    for (let i = 0; i < 100; i++) {
        raindrops[i] = new Rain(random(0, width), random(0, -3000));
    }
}
function letItRain() {
    background(70, 130, 180);
    ground(color(128, 128, 0));
    for (let i = 0; i < raindrops.length; i++) {
        raindrops[i].dropRain();
        raindrops[i].splash();
    }
}





class snowflake {
    constructor(){
        this.posX = 0;
        this.posY = random(-50, 0);
        this.initialangle = random(0, 2 * PI);
        this.size = random(2, 5);
        this.radius = sqrt(random(pow(width / 2, 2)));
    }

    update(time) {
        let w = 0.6;
        let angle = w * time + this.initialangle;
        this.posX = width / 2 + this.radius * sin(angle);

        this.posY += pow(this.size, 0.5);
        if (this.posY > height) {
            let index = snowflakes.indexOf(this);
            snowflakes.splice(index, 1);
        }
    }

    display() {
        stroke(255);
        fill(255);
        ellipse(this.posX, this.posY, this.size);
    }
}

function Rain(x, y) {
    this.x = x;
    this.y = y;
    //this.gravity = 9.8;
    this.length = 15;
    this.r = 0;
    this.opacity = 200;
    this.yy = random(410,430);
    if(this.x > width/2-100 && this.x < width/2+100){
        this.yy = random(380,430);
    }
    if(this.x < 200 && this.x > width -200){
        this.yy = random(425,440);
    }

    this.dropRain = function() {
        noStroke();
        fill(sky_blue);
        //rect(this.x, this.y,3,15);
        ellipse(this.x, this.y, 3, this.length);
        this.y = this.y + 6 //+ frameCount/60;
        if (this.y > this.yy) {
            this.length = this.length - 5;
            //this.y= random(0,-100);
        }
        if (this.length < 0) {
            this.length = 0;
        }
    }

    this.splash = function() {
        strokeWeight(2);
        //stroke(245, 200/frameCount);
        stroke(245, this.opacity);
        noFill();
        if (this.y > this.yy) {
            ellipse(this.x, this.yy, this.r * 2, this.r / 2);
            this.r++;
            this.opacity = this.opacity - 10;

            //keep the rain dropping
            if (this.opacity < 0) {
                this.y = random(0, -100);
                this.length = 15;
                this.r = 0;
                this.opacity = 200;
            }
        }
    }
}

function draw() {
    background(sky_blue);
    ground(color(0,255,0));
    sun();
    //translate(-275, -175);
    //box(85);
    //  alert(obj.strokeArray)
    if(snow){
        background(sky_blue);
        letItSnow();
    } else if(rain){
        letItRain();
    }

    for (let i = 0; i< obj_array.length; i++){

        if(obj_array[i].action != undefined){

            obj_array[i].walk();
        }
        obj_array[i].display();

    }

}

function sun() {
    let a = 20;
    let b =20;
    noStroke();
    fill(255, 255, 0);
    ellipse(a, b + 10, 130, 130);
    strokeWeight(4);
    stroke(255, 255, 0);
    //   line(a + 60, b - 35, 190, 7);
    line(a + 80, b- 10, 210, 20);
    line(a + 75, b+ 20, 200, 90);
    line(a + 60, b+ 55, 170, 150);
    line(a+ 30, b + 80, 100, 200);
    line(a - 10, b + 90, 20, 220);
}