import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Net, NetFactory } from './net/net.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  nets: Net[] = [];
  displayNet: Net;
  dynamicData: any;
  staticData: any;

  constructor(private http: HttpClient) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  ngOnInit() {
    this.getJSON('assets/densities/net1_den1.json').subscribe((dynamicData) => {
      this.dynamicData = dynamicData;
      this.getJSON('assets/nets/net1.json').subscribe(netData => {
        this.staticData = netData;
        for (let dynamicDataExample of dynamicData.values){
          let net: Net = NetFactory.netFromJson(this.staticData,dynamicDataExample);
          this.nets.push(net);
        }
        this.displayNet=this.nets[1];
      })
    })
  }
}
