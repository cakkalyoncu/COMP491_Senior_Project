let obj_array = [];
var c;

let linenums= [];

p5.disableFriendlyErrors = true;
function setup() {
  let list = JSON.parse(document.getElementById('objs').textContent);
  for (let i = 0; i< list.length; i++){
    let a = JSON.parse(list[i]);
  //  let location = getLocation(a);
//alert("hey");
    let w = 10+ ((i%24)*110);
    let h = 10 + ((int)(i/24))*110;
 //   alert("w: "+w+ "h: "+h);
    let obj = new DrawingObject(a.name, a.color, 0.5, a.number, w, h, a.strokeArray, a.id);
    obj_array.push(obj);
   //  alert("obj_array")
  }

 c = createCanvas(1460,700);
 output = createGraphics(1460, 700);
 output.background(225)
}

function newPage() {
    //saveCanvas(c, 'myCanvas', 'jpg');
    output.save("output.png");
    c.clear()
    output.clear()
}

function draw() {
    //translate(-275, -175);
  //box(85);
 //   alert(obj_array.length)
   // alert("obj_array: " + obj_array.length);
 //   alert(obj_array.length);
  for (let i = 0; i< obj_array.length; i++){
   //   alert(i);
    obj_array[i].display();


          if(obj_array.length == 1){
          alert(obj_array[i].id);
      }
  }
}

function mouseClicked() {
    let i= (int)((mouseX )/55);
    let j = (int)((mouseY)/55);
    let imageNum=(j*24)+i+1;
    linenums.push(imageNum);
    if(linenums.length>=5){
        alert(linenums);
    }
}


class DrawingObject {
  constructor(name, color, size, number, location_X, location_Y, strokeArray, id) {
      this.id=id;
    this.ready= 0;
    this.name =name;
    this.color= color;
    this.size= size;
    this.number= number;
    this.index = 0;
    this.strokeIndex = 0;
    this.location_X = location_X;
    this.location_Y = location_Y;
    strokeArray = this.normalize(strokeArray);
    this.strokeArray = strokeArray;
  }

  normalize(strokeArray){
      let minx = 1000;
      let miny = 1000;
      let maxx = 0;
      let maxy = 0;
      for(let j=0; j < strokeArray.length; j++) {
          for(let i=0; i < strokeArray[j][0].length; i++) {
                let x = strokeArray[j][0][i];
                let y = strokeArray[j][1][i];
                if (x < minx){
                    minx = x;
                }
                if (y < miny){
                    miny = y;
                }
                if (x > maxx){
                    maxx = x;
                }
                if (y > maxy){
                    maxy = y;
                }
          }
      }

      let ratiox = (maxx - minx)/100;

      let ratioy = (maxy - miny)/100;
 //      alert("ratiox:" + ratiox );
 //       alert("ratioy:" + ratioy );
      for(let j=0; j < strokeArray.length; j++) {
          for(let i=0; i < strokeArray[j][0].length; i++) {
                strokeArray[j][0][i] = (strokeArray[j][0][i] - minx) / ratiox;
                strokeArray[j][1][i] = (strokeArray[j][1][i] - miny) / ratioy;
          }
      }
 //     alert("strokeArray:" + strokeArray );
      return strokeArray;
  }


    display() {
for(let path of this.strokeArray){
        stroke(this.color);
        fill(this.color)
        strokeWeight(3);
        beginShape();
        for(let i = 0; i< path[0].length; i++){
            let x = path[0][i] + this.location_X;
            x = x * this.size;
            let y = path[1][i] + this.location_Y;
            y = y * this.size;
            vertex(x,y);
        }
        endShape();
      }


  }
}