import { Injectable } from '@angular/core';
import { Point } from './net.model';
 

@Injectable({
  providedIn: 'root'
})
export class NetService {
  ctx: CanvasRenderingContext2D

  constructor() { }
     roundRectangle(x, y, width, height, radius) {
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
  perpendicularLine(point,lineStart,lineEnd){
    const a=(lineEnd.y-lineStart.y)/(lineEnd.x-lineStart.x)
    const aT= -1/a
    const angle=Math.atan(aT);
    const r=10 // line length
    this.ctx.lineTo(point.x + r * Math.cos(angle), point.y + r * Math.sin(angle));
    this.ctx.lineTo(point.x - r * Math.cos(angle), point.y - r * Math.sin(angle));
}
  putText(startPoint,endPoint,text){
    const a=(endPoint.y-startPoint.y)/(endPoint.x-startPoint.x)
    const middlePointX=(startPoint.x+endPoint.x)/2
    const middlePointY=(startPoint.y+endPoint.y)/2
    if(a<-0.5 || a > 0.5){
        this.ctx.fillText(text,middlePointX-10,middlePointY);
    }
    else{
      this.ctx.fillText(text,middlePointX,middlePointY-10);
    }
}
  line(start,end,texts,divisions){
    let oldPoint;
    this.ctx.moveTo(start.x, start.y);
    if(divisions){
        for(let i=0;i<=divisions;i++){
            let x=(end.x-start.x)/divisions*i+start.x;
            let y=(end.y-start.y)/divisions*i+start.y;
            this.ctx.lineTo(x,y);
            this.perpendicularLine(new Point(x,y),start,end);
            if(i>=1){
                this.putText(oldPoint,new Point(x,y),texts[i-1]);
            }
            this.ctx.lineTo(x,y)
            oldPoint = new Point(x,y)
        }
    }
    else{
      this.ctx.lineTo(end.x,end.y);  
    }
  }

}
