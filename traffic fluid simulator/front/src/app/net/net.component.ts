import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, Input } from '@angular/core';
import { CanvasService } from '../canvas.service';
import { Net } from 'src/model/net';
@Component({
  selector: 'app-net',
  templateUrl: './net.component.html',
  styleUrls: ['./net.component.css']
})
export class NetComponent implements AfterViewInit {
  @ViewChild('netCanvas')
  netCanvas: ElementRef;
  @Input()
  set net(v: Net) {
    this._net = v;
    if (this._net) {
      this.drawNet();
    }
  }
  private _net: Net;
  get net(): Net{
    return this._net;
  }
  ctx: CanvasRenderingContext2D;
  mousePosition;
  constructor(private cs: CanvasService) { }
  ngAfterViewInit() {
    this.ctx = this.netCanvas.nativeElement.getContext("2d");
    this.cs.ctx = this.ctx;
    this.cs.netCanvas = this.netCanvas;
    this.netCanvas.nativeElement.addEventListener("mousemove",
      (evt)=>this.getMousePos(evt)
      );
  }

  drawNet() {
    this.ctx.clearRect(0, 0, this.netCanvas.nativeElement.width, this.netCanvas.nativeElement.height);
    this.cs.drawAllLines(this._net);
    this.ctx.stroke();
  }
  getMousePos(evt) {
    let rect = this.netCanvas.nativeElement.getBoundingClientRect();
    this.mousePosition = {
      x: Math.round(evt.clientX - rect.left),
      y: Math.round(evt.clientY - rect.top)
    };
}

}
