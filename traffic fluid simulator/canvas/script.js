class Point{
    constructor(x,y){
        this.x=x;
        this.y=y;
    }
}
function roundRectangle(ctx,x, y, width, height, radius, fill) {
  if (typeof radius === "undefined") {
    radius = 5;
  }
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  if (fill) {
    ctx.fill();
  }        
}
function perpendicularLine(ctx,point,lineStart,lineEnd){
    a=(lineEnd.y-lineStart.y)/(lineEnd.x-lineStart.x)
    aT= -1/a
    angle=Math.atan(aT);
    r=10 // line length
    ctx.lineTo(point.x + r * Math.cos(angle), point.y + r * Math.sin(angle));
    ctx.lineTo(point.x - r * Math.cos(angle), point.y - r * Math.sin(angle));
}
function putText(ctx,startPoint,endPoint,text){
    a=(endPoint.y-startPoint.y)/(endPoint.x-startPoint.x)
    middlePointX=(startPoint.x+endPoint.x)/2
    middlePointY=(startPoint.y+endPoint.y)/2
    if(a<-0.5 || a > 0.5){
        ctx.fillText(text,middlePointX-10,middlePointY);
    }
    else{
        ctx.fillText(text,middlePointX,middlePointY-10);
    }

}
function line(ctx,start,end,texts,divisions){
    ctx.moveTo(start.x, start.y);
    if(divisions){
        for(i=0;i<=divisions;i++){
            if(i>=1){
                oldPoint = new Point(x,y)
            }
            x=(end.x-start.x)/divisions*i+start.x;
            y=(end.y-start.y)/divisions*i+start.y;
            ctx.lineTo(x,y)
            perpendicularLine(ctx,new Point(x,y),start,end);
            if(i>=1){
                putText(ctx,oldPoint,new Point(x,y),texts[i-1]);
            }
            ctx.lineTo(x,y)
        }
    }
    else{
        ctx.lineTo(end.x,end.y);  
    }
}
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
line(ctx,new Point(100,300),new Point(200,300),[1,2],2)
line(ctx,new Point(300,270),new Point(400,230),[1,2],2)
line(ctx,new Point(300,330),new Point(400,370),[1,2],2)
ctx.stroke()
roundRectangle(ctx,210,260,80,80,10)
ctx.stroke()
ctx.drawArrow
// ctx.font = "12px Arial";
