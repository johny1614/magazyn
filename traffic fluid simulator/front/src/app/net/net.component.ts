import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { NetService } from './net.service';
import { Point, Line, LightsSignalization, Light, LightPositioned, Net, NetFactory } from './net.model';
import { CanvasService } from '../canvas.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
// import data  from '../../assets/nets/net1';
@Component({
  selector: 'app-net',
  templateUrl: './net.component.html',
  styleUrls: ['./net.component.css']
})
export class NetComponent implements AfterViewInit {
  @ViewChild('net')
  netCanvas: ElementRef;
  net: Net;
  ctx: CanvasRenderingContext2D;
  constructor(private ns: NetService, private cs: CanvasService, private http: HttpClient) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }

  ngAfterViewInit() {
    // console.log('data to',this.json);
    this.getJSON('assets/nets/net1.json').subscribe(data => {
      this.ctx = this.netCanvas.nativeElement.getContext("2d");
      this.cs.ctx = this.ctx;
      this.net = data;
      const line1 = NetFactory.getLine(this.net.lines[0]);
      console.log('l1', line1);
      const line2 = NetFactory.getLine(this.net.lines[1]);
      const line3 = NetFactory.getLine(this.net.lines[2]);
      this.net.lines = [line1, line2, line3];
      this.cs.drawAllLines(this.net);
      this.ctx.stroke();
    });
    // this.ns.ctx = this.ctx;
    // const lights1=new LightsSignalization();
    // lights1.left=new LightPositioned(Light.green,new Point(215, 285),'right_up_green')
    // lights1.right=new LightPositioned(Light.green,new Point(215, 305),'right_down_green')
    // const line1 = new Line(new Point(100, 300), new Point(200, 300), [2, 1],lights1)
    // const line3 = new Line(new Point(300, 330), new Point(400, 370), [1, 2])
    // const line2 = new Line(new Point(300, 270), new Point(400, 230), [1, 2])
    // const net = new Net(0,[line1,line2,line3]);
    // this.cs.drawAllLines(net);
    // this.ctx.stroke();
    // this.ns.roundRectangle(210, 260, 80, 80, 10)
    // this.ctx.stroke();
  }

}
