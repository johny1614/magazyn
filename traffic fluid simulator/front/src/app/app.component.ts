import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Net, NetFactory, Line } from './net/net.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  nets: Net[] = [];
  dynamicData: any;
  staticData: any;
  timeDisplay;

  constructor(private http: HttpClient) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  ngOnInit() {
    this.getJSON('assets/nets/net2.json').subscribe(netData => {
      this.staticData = netData;
      this.getJSON('assets/densities/net2_den1_python.json').subscribe(dynamicData => {
        for (let i = 0; i < dynamicData.nets.length; i++) {
          let staticNet = NetFactory.netFromJson(this.staticData);
          let dynamicNet = dynamicData.nets[i];
          let k = 0;
          for (let line of staticNet.lines) {
            for (let section of line.sections) {
              section.density = dynamicNet.densities[k]
              k++;
            }
          }
          this.nets.push(staticNet);
        }
      })
    });
  }
}
