let obj_array = [];
let pause = false;
let sky_blue;
let snowflakes = [];
let raindrops = [];
let clouds = [];
let snow = false;
let rain = false;
let cloudy = false;
var image = new Image();
let speed;
let time;
let memory;
let indoor= new Image();
let indoor_bool = false;

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
    let loc_arr_big_sky = [{"x":50, "y":67},{"x":250, "y":79}, {"x":450, "y":63} ]
    let loc_arr_sky = [{"x":50, "y":100},{"x":250, "y":110}, {"x":450, "y":120}, {"x":650, "y":125}, {"x":850, "y":130} ]
    let loc_arr_small_sky = [{"x":10, "y":110}, {"x":300, "y":130}, {"x":600, "y":140}, {"x":850, "y":155}, {"x":1250, "y":167} , {"x":1450, "y":185}, {"x":1750, "y":190} ]
    let loc_arr_big_ground = [{"x":50, "y":170},{"x":250, "y":163}, {"x":450, "y":160} ]
    let loc_arr_ground = [{"x":50, "y":320},{"x":250, "y":300}, {"x":450, "y":290}, {"x":650, "y":300}, {"x":850, "y":320} ]
    let loc_arr_small_ground = [{"x":10, "y":715}, {"x":300, "y":695}, {"x":600, "y":690}, {"x":850, "y":685}, {"x":1250, "y":695} , {"x":1450, "y":700}, {"x":1750, "y":720} ]
    let loc = json_obj.location;
    //    alert(json_obj.action);
    if(loc == "random" || loc.Location=="house"){
        let x = randomIntFromInterval(300,400);
        let y;
        if(json_obj.action == null || json_obj.action == undefined || json_obj.action["Action"] =="walk" || json_obj.action["Custom"] ){
            y = randomIntFromInterval(300,330);
            if(json_obj.size ==1.5){
                let index = randomIntFromInterval(0,2);
                x = loc_arr_big_ground[index]["x"];
                y = loc_arr_big_ground[index]["y"];
            } else if(json_obj.size ==0.5){
                let index = randomIntFromInterval(0,6);
                x = loc_arr_small_ground[index]["x"];
                y = loc_arr_small_ground[index]["y"];
            } else if(json_obj.size ==1){
                let index = randomIntFromInterval(0,4);
                x = loc_arr_ground[index]["x"];
                y = loc_arr_ground[index]["y"];
            }
        }
        else{
            y = randomIntFromInterval(100,130);
            if(json_obj.size ==1.5){
                let index = randomIntFromInterval(0,2);
                x = loc_arr_big_sky[index]["x"];
                y = loc_arr_big_sky[index]["y"];
            } else if(json_obj.size ==1){
                let index = randomIntFromInterval(0,4);
                x = loc_arr_sky[index]["x"];
                y = loc_arr_sky[index]["y"];
            } else if(json_obj.size ==0.5){
                let index = randomIntFromInterval(0,6);
                x = loc_arr_small_sky[index]["x"];
                y = loc_arr_small_sky[index]["y"];
            }
        }

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
function clearStorage(){
  localStorage.clear();
}


let width = 1060;
let height = 450;

function setup() {
    if(window.localStorage.getItem("pagecount")== null){
        localStorage.setItem("pagecount", "0");
    }
    if (parseInt(window.localStorage.getItem("pagecount"),10)>=1){
        let pages=parseInt(window.localStorage.getItem("pagecount"),10);
        for(let i=0;i<pages;i++){
            document.getElementById("p"+i).src=localStorage.getItem("p"+i);
        }
    }
    if(window.localStorage.getItem("title")!= null){
        document.getElementById("title").textContent =localStorage.getItem("title");
    }

    memory =0;
    speed = true;
    time = 0;
    prepareRain();
    prepareClouds();
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
            cloudy = false;
        } else if(weather=="rain"){
            snow = false;
            rain = true;
            cloudy = false;
        } else if(weather=="sun"){
            snow = false;
            rain = false;
            cloudy = false;
        } else if(weather=="cloud"){
            snow = false;
            rain = false;
            cloudy = true;
        }
    }
    for (let i = 0; i< list.length; i++){
        let a = JSON.parse(list[i]);
        //       alert(a.action);


        let location = getLocation(a);
        if(a.location.Location=="house"){
            indoor = loadImage("../static/museum_imgs/indoor.jpg");
            indoor_bool = true;
        }
        for(let m =0; m< a.number; m++){

            let w = location[0]+ (m * 120);
            let h = location[1];
            //    alert(a.name+" : "+ a.number+ " w: "+w);
            //let obj = new DrawingObject(a.name, a.color, a.size, a.number, w, h, a.strokeArray, a.action);
            //alert(a.file_path);
            let obj;
            if(a.file_path == null || a.file_path == undefined){

                obj = new DrawingObject(a.name, a.color, a.size, a.number, w, h, a.strokeArray, a.action);

            }else{
                obj = new ImageObject(a.name, a.size, a.number, w, h, a.file_path, a.action);
            }

            obj_array.push(obj);
        }

        time=0;
    }
    var canvas = createCanvas(width,height);
    canvas.parent("sketchholder");
    frameRate(20);
}



function newPage() {
    image.src = canvas.toDataURL("image/png");
    let pc= parseInt(window.localStorage.getItem("pagecount"),10);
    let imgstring="p"+pc+"";
    localStorage.setItem(imgstring, image.src);
    let newcount=pc+1;
    localStorage.setItem("pagecount", newcount);
    localStorage.setItem("title",  document.getElementById("title").textContent);
    canvas.clear();
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
    if(indoor_bool){
        image(indoor, 0 , 0,   width ,  height);
    }
    //translate(-275, -175);
    //box(85);
    if(snow){
        background(sky_blue);
        letItSnow();
    } else if(rain){
        letItRain();
    } else if(cloudy){
        drawClouds();
    }

    for (let i = 0; i< obj_array.length; i++)   {

        if(obj_array[i].action != null && obj_array[i].action != undefined && obj_array[i].action != "") {
            if (obj_array[i].action["Custom"]) {

                let l = obj_array[i].action["Action"].length;
                if (obj_array[i].action["Action"][time % l] == "fly" && speed) {
                    obj_array[i].fly();
                } else if (obj_array[i].action["Action"][time % l] == "ascend" && speed) {
                    obj_array[i].ascend();
                } else if (obj_array[i].action["Action"][time % l] == "goRight" && speed) {
                    obj_array[i].goRight();
                } else if (obj_array[i].action["Action"][time % l] == "goLeft" && speed) {
                    obj_array[i].goLeft();
                }

            } else {
                obj_array[i].walk();
            }
        }

        //alert(obj_array[i].name);
        obj_array[i].display();

    }
    if (speed) {
            time += 1;
            speed = false;
        } else {
            speed = true;
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
function drawClouds(){
    background(color(173,216,230));
    ground(color(0,255,0));
    for(let i = 0; i< clouds.length; i++){
        cloud(clouds[i].xpos, clouds[i].ypos, clouds[i].size);
    }
}
function prepareClouds(){
    for(let j = 0; j<15; j++){
        var newCloud = { xpos: random(10, 1000), ypos: random(50, 110), size: random(1, 3)};
        clouds.push(newCloud);
    }
}
function cloud(x, y, size) {
    fill(255, 255, 255);
    noStroke();
    arc(x, y, 25 * size, 20 * size, PI + TWO_PI, TWO_PI);
    arc(x + 10, y, 25 * size, 45 * size, PI + TWO_PI, TWO_PI);
    arc(x + 25, y, 25 * size, 35 * size, PI + TWO_PI, TWO_PI);
    arc(x + 40, y, 30 * size, 20 * size, PI + TWO_PI, TWO_PI);
}
