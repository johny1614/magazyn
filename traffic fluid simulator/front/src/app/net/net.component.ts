import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { NetService } from './net.service';
import { Point, Line, LightsSignalization, Light, LightPositioned } from './net.model';
import { CanvasService } from '../canvas.service';

@Component({
  selector: 'app-net',
  templateUrl: './net.component.html',
  styleUrls: ['./net.component.css']
})
export class NetComponent implements AfterViewInit {
  @ViewChild('net')
  net: ElementRef;
  ctx: CanvasRenderingContext2D;
  constructor(private ns: NetService, private cs: CanvasService) { }

  ngAfterViewInit() {
    this.ctx = this.net.nativeElement.getContext("2d");
    this.ns.ctx = this.ctx;
    this.cs.ctx = this.ctx;
    const lights1=new LightsSignalization();
    lights1.left=new LightPositioned(Light.green,new Point(215, 285),'right_up_green')
    lights1.right=new LightPositioned(Light.green,new Point(215, 305),'right_down_green')
    const line1 = new Line(new Point(100, 300), new Point(200, 300), [2, 1],lights1)
    const line2 = new Line(new Point(300, 270), new Point(400, 230), [1, 2])
    const line3 = new Line(new Point(300, 330), new Point(400, 370), [1, 2])
    this.cs.drawLine(line1);
    this.cs.drawLine(line2);
    this.cs.drawLine(line3);
    this.ctx.stroke();
    this.ns.roundRectangle(210, 260, 80, 80, 10)
    this.ctx.stroke();
  }

}
