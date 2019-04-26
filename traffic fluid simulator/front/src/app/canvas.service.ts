import { Injectable } from '@angular/core';
import { Line } from 'src/model/line';
import { SingleLight } from 'src/model/light';
import { Net } from 'src/model/net';



@Injectable()
export class CanvasService {
  ctx: CanvasRenderingContext2D

  constructor() { }
  drawRoundRectangle(x, y, width, height, radius) {
    if (typeof radius === "undefined") {
      radius = 5;
    }
    this.ctx.beginPath();
    this.ctx.moveTo(x + radius, y);
    this.ctx.lineTo(x + width - radius, y);
    this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    this.ctx.lineTo(x + width, y + height - radius);
    this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    this.ctx.lineTo(x + radius, y + height);
    this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    this.ctx.lineTo(x, y + radius);
    this.ctx.quadraticCurveTo(x, y, x + radius, y);
    this.ctx.closePath();
  }
  drawPerpendicularLine(point, a) { // a is of a base line to which function draws a perpendicular line
    const aT = -1 / a
    const angle = Math.atan(aT);
    const r = 10 // line length
    this.ctx.moveTo(point.x, point.y);
    this.ctx.lineTo(point.x + r * Math.cos(angle), point.y + r * Math.sin(angle));
    this.ctx.lineTo(point.x - r * Math.cos(angle), point.y - r * Math.sin(angle));
    this.ctx.moveTo(point.x, point.y);
  }
  writeDensity(section) {
    this.ctx.font = "20px Arial";
    if (section.a < -0.5 || section.a > 0.5) {
      this.ctx.fillText(section.density, section.middlePoint.x - 10, section.middlePoint.y);
    }
    else {
      this.ctx.fillText(section.density, section.middlePoint.x - 5, section.middlePoint.y - 10);
    }
  }
  drawLights(line: Line) {
    Object.keys(line.lights).forEach(
      direction => {
        const light: SingleLight = line.lights[direction];
        console.log(light.rotation)
        let arrowImage = new Image();
        arrowImage.src = "../../assets/arrows/" + light.imageName + ".png";
        arrowImage.onload = () => {
          const width = light.arrowWidth ? light.arrowWidth : 40;
          const scaledHeight = width * arrowImage.height / arrowImage.width
          if (light.rotation > 0) {
            this.ctx.save();
            const rotateValue = light.rotation * Math.PI / 180
            // const rotateValue = 20 * Math.PI / 180;
            console.log(rotateValue);
            
            this.ctx.rotate(rotateValue)
            this.ctx.drawImage(arrowImage, light.position.x, light.position.y, width, scaledHeight);
            this.ctx.restore();
          }
          else {
            // this.ctx.drawImage(arrowImage, light.position.x, light.position.y, width, scaledHeight);

          }
          // this.ctx.save();
          // this.ctx.rotate(Math.PI)
          // this.ctx.restore();


          // ctx.save(); // save current state
          // ctx.rotate(Math.PI); // rotate
          // ctx.drawImage(link,x,y,20,20); // draws a chain link or dagger
          // ctx.restore(); // restore original states (no rotation etc)

        }
      }
    )
  }
  drawLine(line: Line) {
    this.ctx.moveTo(line.startPoint.x, line.startPoint.y);
    for (let i = 0; i < line.sections.length; i++) {
      const section = line.sections[i];
      this.ctx.moveTo(section.startPoint.x, section.startPoint.y);
      this.ctx.lineTo(section.endPoint.x, section.endPoint.y);
      this.drawPerpendicularLine(section.endPoint, section.a);
      this.writeDensity(section);
      if (i === 0) {
        this.drawPerpendicularLine(section.startPoint, section.a);
      }
    }
    if (line.lights) {
      this.drawLights(line);
    }
  }
  drawAllLines(net: Net) {
    for (let line of net.lines) {
      this.drawLine(line);
    }
  }
}
