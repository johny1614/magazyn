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
  @ViewChild('netCanvas')
  netCanvas: ElementRef;

  net: Net;
  ctx: CanvasRenderingContext2D;
  constructor(private ns: NetService, private cs: CanvasService, private http: HttpClient) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  ngAfterViewInit() 
  {
    this.getJSON('assets/nets/net1.json').subscribe(netData => {
      this.getJSON('assets/densities/net1_den1.json').subscribe(dynamicData=>{
        this.ctx = this.netCanvas.nativeElement.getContext("2d");
        this.net=NetFactory.netFromJson(netData,dynamicData);
        this.cs.ctx = this.ctx;
        this.cs.drawAllLines(this.net);
        this.ctx.stroke();
        
      })
    });
  }

}
