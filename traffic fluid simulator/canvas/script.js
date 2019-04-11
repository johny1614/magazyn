class Point{
    constructor(x,y){
        this.x=x;
        this.y=y;
    }
}
function line(ctx,start,end,text,divisions){
    ctx.moveTo(start.x, start.y);
    if(divisions){
        for(i=1;i<=divisions;i++){
            x=start.x+end.x*i/divisions;
            y=start.y+end.y*i/divisions;
            console.log(y);
            ctx.lineTo(x,y)
        }
    }
    else{
        ctx.lineTo(end.x,end.y);  
    }
}
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
a=line(ctx,new Point(0,600),new Point(200,600),"",6)
line(ctx,new Point(0,400),new Point(200,400))
ctx.stroke()
ctx.font = "12px Arial";
