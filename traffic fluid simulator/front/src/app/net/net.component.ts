import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, Input } from '@angular/core';
import { NetService } from './net.service';
import { Point, Line, LightsSignalization, Light, LightPositioned, Net, NetFactory } from './net.model';
import { CanvasService } from '../canvas.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
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
  ctx: CanvasRenderingContext2D;
  constructor(private cs: CanvasService) { }
  ngAfterViewInit() {
    this.ctx = this.netCanvas.nativeElement.getContext("2d");
    this.cs.ctx = this.ctx;
  }

  drawNet() {
    this.cs.drawAllLines(this._net);
    this.ctx.stroke();
  }

}
