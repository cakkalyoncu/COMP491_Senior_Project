const url1 = 'https://quickdrawfiles.appspot.com/drawing/'
const url2 = '?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated=false&format=JSON'
let bug; // Declare object
let data;
let bug2;

function preload() {
  let thingname = JSON.parse(document.getElementById('object').textContent);
  //let url = url1+thingname+url2;
  //alert(url);
  data = loadJSON("https://quickdrawfiles.appspot.com/drawing/cat?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated=false&format=JSON");
  data2 = loadJSON("https://quickdrawfiles.appspot.com/drawing/cat?&key=AIzaSyC1_soqtXV1mTyetVpJ4GglGD5RtXuFp4o&isAnimated=false&format=JSON");
}


function setup() {
  createCanvas(710, 400);
  // Create object
  let color1 =  color(0,0,255);
  let color2 =  color(0,255,0);
  bug = new DrawingObject(data,100,100,color1);
  bug2 = new DrawingObject(data2,0,0,color2);
}

function draw() {

  bug.display();
  bug2.display();

}

// Jitter class
class DrawingObject {
  constructor(data, location_X, location_Y, color) {
    this.ready= 0;
    //this.name =name;
    this.index = 0;
    this.strokeIndex = 0;
    this.location_X = location_X;
    this.location_Y = location_Y;
    this.strokeArray = data.drawing;
    this.diameter = random(10, 30);
    this.speed = 1;
    this.color= color;
    // alert(this.color);


  }


    display() {
//alert(this.strokeArray.length);
  for(let i=0; i <= this.strokeArray[this.strokeIndex][0].length; i++){
      let x = this.strokeArray[this.strokeIndex][0][this.index]+this.location_X ;
      let y = this.strokeArray[this.strokeIndex][1][this.index]+this.location_Y;
      stroke(this.color);
      if (this.prevx !== undefined) {
        line(this.prevx, this.prevy, x, y);
      }
      this.index++;
      if (this.index === this.strokeArray[this.strokeIndex][0].length) {
      this.strokeIndex++;
      this.prevx = undefined;
      this.prevy = undefined;
      this.index = 0;
      if (this.strokeIndex === this.strokeArray.length) {
        this.strokeArray = undefined;
        this.strokeIndex = 0;
      }
    } else {
      this.prevx = x;
      this.prevy = y;
    }
  }

  }
}