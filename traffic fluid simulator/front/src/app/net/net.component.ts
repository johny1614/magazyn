import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, Input } from '@angular/core';
import { CanvasService } from '../canvas.service';
import { Net } from 'src/model/net';
import { NetFactory } from 'src/services/netFactory';
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
    console.log('e', this._net.lines[0].densities[0])
    this._net.lines[0].densities[0] = 12
    console.log('b', this._net.lines[0].densities[0])
    if (this._net) {
      console.log('draw!')
      this.drawNet();
    }
  }
  private _net: Net;
  get net(): Net {
    return this._net;
  }
  ctx: CanvasRenderingContext2D;
  mousePosition;
  constructor(private cs: CanvasService) { }
  ngAfterViewInit() {
    // this._net.lines[0].densities[0]=17
    this.ctx = this.netCanvas.nativeElement.getContext("2d");
    this.cs.ctx = this.ctx;
    this.cs.netCanvas = this.netCanvas;
    this.netCanvas.nativeElement.addEventListener("mousemove",
      (evt) => this.getMousePos(evt)
    );
  }
  refresh() {
    this.ctx = this.netCanvas.nativeElement.getContext("2d");
    this.cs.ctx = this.ctx;
    this.cs.netCanvas = this.netCanvas;
    this.drawNet();

  }

  setFixedLights() {

    // moves=[((9, 2), (21, 2), (27, 17)),
    //   ((21, 20), (27, 20), (9, 2)),
    //   ((27, 17), (9, 17), (21, 20))],

    this.net.A[21][20] = 1 // powinno byc 0.7 ale jbc
    this.net.A[27][17] = 1
    this.net.A[9][17] = 1
    this.net = NetFactory.changeLights(this.net)
    console.log('po zmianie',this.net)
    // this.net.lines[6].lights.left=1
    // this.net.lines[6].lights.straight=1
    // this.net.lines[6].lights.right=1

  }
  setFixedDensities() {
    let x = [2, 2, 2, 10, 20, 30, 0, 0, 0, + 1]

    this.net.lines[0].sections[0].density = x[0]
    this.net.lines[0].sections[1].density = x[1]
    this.net.lines[0].sections[2].density = x[2]

    this.net.lines[6].sections[0].density = x[3]
    this.net.lines[6].sections[1].density = x[4]
    this.net.lines[6].sections[2].density = x[5]

    this.net.lines[7].sections[0].density = x[6]
    this.net.lines[8].sections[0].density = x[7]
    this.net.lines[9].sections[0].density = x[8]

  }

  drawNet() {
    this.ctx.clearRect(0, 0, this.netCanvas.nativeElement.width, this.netCanvas.nativeElement.height);
    console.log('rysuje wedle', this._net)
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
