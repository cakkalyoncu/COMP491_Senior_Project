//general object parent
class GenObject {
    constructor(name,size,number,location_X, location_Y, action) {
        this.name = name;
        this.size = size;
        this.number = number;
        this.location_X = location_X;
        this.location_Y = location_Y;
        this.start_Y = location_Y;
        this.speed = 10;
        this.direction = Math.random() < 0.5;
        this.action = action;
    }

    move() {
        this.location_X += random(-10, 10);
        this.location_Y += random(-10, 10);
    }

    walk() {
        //     alert(1060 - (this.size*105));
        if (this.location_X <= 5 || (this.size == 1.5 && this.location_X >= 600) || (this.size == 0.5 && this.location_X >= 2030) || (this.size == 1 && this.location_X >= 1060 - 105)) {
            this.direction = !this.direction;
        }
        if (this.direction) {
            this.location_X -= 10;
        } else {
            this.location_X += 10;
        }
        this.location_Y += random(-5, 5);
        if (this.location_Y > this.start_Y + 20) {
            this.location_Y -= 5;
        } else if (this.location_Y < this.start_Y - 20) {
            this.location_Y += 5;
        }

    }

    fly() {
       this.location_Y -= 30;
    }
     ascend() {
       this.location_Y += 30;
    }
    goLeft() {
       this.location_X -= 30;
    }
    goRight() {
       this.location_X += 30;
    }
}

class DrawingObject extends GenObject{
    constructor(name, color, size, number, location_X, location_Y, strokeArray, action) {
        super(name,size,number,location_X ,location_Y ,action);
        this.ready = 0;
        this.color = color;
        this.index = 0;
        this.strokeIndex = 0;
        strokeArray = this.normalize(strokeArray);
        this.strokeArray = strokeArray;
    }


    normalize(strokeArray) {
        let minx = 1000;
        let miny = 1000;
        let maxx = 0;
        let maxy = 0;
        for (let j = 0; j < strokeArray.length; j++) {
            for (let i = 0; i < strokeArray[j][0].length; i++) {
                let x = strokeArray[j][0][i];
                let y = strokeArray[j][1][i];
                if (x < minx) {
                    minx = x;
                }
                if (y < miny) {
                    miny = y;
                }
                if (x > maxx) {
                    maxx = x;
                }
                if (y > maxy) {
                    maxy = y;
                }
            }
        }

        let ratiox = (maxx - minx) / 100;

        let ratioy = (maxy - miny) / 100;
        for (let j = 0; j < strokeArray.length; j++) {
            for (let i = 0; i < strokeArray[j][0].length; i++) {
                strokeArray[j][0][i] = (strokeArray[j][0][i] - minx) / ratiox;
                strokeArray[j][1][i] = (strokeArray[j][1][i] - miny) / ratioy;
            }
        }
//      alert("strokeArray:" + strokeArray );
        return strokeArray;
    }

    display() {
        for (let path of this.strokeArray) {
            stroke(this.color);
            fill(this.color)
            strokeWeight(3);
            beginShape();
            for (let i = 0; i < path[0].length; i++) {
                let x = path[0][i] + this.location_X;
                x = x * this.size;
                let y = path[1][i] + this.location_Y;
                y = y * this.size;
                vertex(x, y);
            }
            endShape();
        }
    }
}

class ImageObject extends GenObject{
     constructor(name, size, number, location_X, location_Y, img_path, action) {
        super(name,size, number, location_X ,location_Y ,action);
        this.img = loadImage(img_path);
    }

    display(){
         image(this.img, this.location_X , this.location_Y,  80 * this.size ,  80 * this.size);
    }
}