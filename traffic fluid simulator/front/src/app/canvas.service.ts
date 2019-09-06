import {ElementRef, Injectable} from '@angular/core';
import {Line} from 'src/model/line';
import {LightsSignalization, SingleLight} from 'src/model/light';
import {Net} from 'src/model/net';
import {Point} from "../model/point";


@Injectable()
export class CanvasService {
  ctx: CanvasRenderingContext2D;
  netCanvas: ElementRef;

  constructor() {
  }

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
    // this.ctx.font = "32px Arial"; # dla polibudy
    let densityRounded = Math.round(section.density).toString();
    // console.log('sec',section)
    console.log('sec',section)
    if(section.x_move){
      console.log('jest x move')
      this.ctx.fillText(densityRounded, section.middlePoint.x+section.x_move, section.middlePoint.y);

    }
    else if (section.a < -0.5 || section.a > 0.5) {
      this.ctx.fillText(densityRounded, section.middlePoint.x, section.middlePoint.y);
    }
    else {
      this.ctx.fillText(densityRounded, section.middlePoint.x - 5, section.middlePoint.y - 10);
    }
  }

  drawRotatedImage(degrees: number, image: HTMLImageElement,position: Point,width) {
    const scaledHeight = width * image.height / image.width;
    this.ctx.save();
    this.ctx.translate(position.x+image.width / 2,position.y);
    this.ctx.rotate(degrees * Math.PI / 180);
    this.ctx.drawImage(image, -image.width / 2, -image.width / 2,width,scaledHeight);
    this.ctx.restore();
  }

  drawLights(line: Line) {
    // console.log('LINIA',line)
    Object.keys(line.lights).forEach(
      direction => {
        const light: SingleLight = line.lights[direction];
        // console.log('light',light)
        let arrowImage = new Image();
        arrowImage.src = "../../assets/arrows/" + light.imageName + ".png";
        arrowImage.onload = () => {
          const width = light.arrowWidth ? light.arrowWidth : 40;
          const scaledHeight = width * arrowImage.height / arrowImage.width;
          if (light.rotation > 0) {
            this.drawRotatedImage(light.rotation, arrowImage,light.position,width);
          }
          else {
            this.ctx.drawImage(arrowImage, light.position.x, light.position.y, width, scaledHeight);
          }
        }
      }
    )
  }

  drawLine(line: Line) {
    this.ctx.moveTo(line.startPoint.x, line.startPoint.y);
    this.ctx.lineWidth=1
    // this.ctx.lineWidth=3 // dla poli
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
    // console.log('serwis ma neta',net)
    for (let line of net.lines) {
      this.drawLine(line);
    }
  }
}
