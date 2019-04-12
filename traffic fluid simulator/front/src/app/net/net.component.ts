import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { NetService, Point } from './net.service';

@Component({
  selector: 'app-net',
  templateUrl: './net.component.html',
  styleUrls: ['./net.component.css']
})
export class NetComponent implements AfterViewInit {
  @ViewChild('net')
  net: ElementRef;
  ctx: CanvasRenderingContext2D;
  constructor(private ns: NetService) { }

  ngAfterViewInit() {
    this.ctx = this.net.nativeElement.getContext("2d");
    this.ns.ctx = this.ctx;
    this.ns.line(new Point(100, 300), new Point(200, 300), [1, 2], 2)
    this.ns.line(new Point(300, 270), new Point(400, 230), [1, 2], 2)
    this.ns.line(new Point(300, 330), new Point(400, 370), [1, 2], 2)
    this.ctx.stroke();
    this.ns.roundRectangle(210,260,80,80,10)
    this.ctx.stroke();
  }

}
