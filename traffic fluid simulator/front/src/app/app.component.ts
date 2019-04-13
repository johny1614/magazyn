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
  dynamicData: any;
  staticData: any;
  timeDisplay;

  constructor(private http: HttpClient) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  ngOnInit() {
    // this.getJSON('assets/densities/net1_den1.json').subscribe((dynamicData) => {
      //   this.dynamicData = dynamicData;
        this.getJSON('assets/nets/net2.json').subscribe(netData => {
            this.staticData = netData;
            let net: Net = NetFactory.netFromJson(this.staticData);
            console.log('necik pusty',net);
            this.nets.push(net);
        });

            // for (let dynamicDataExample of dynamicData.values){
            //     let net: Net = NetFactory.netFromJson(this.staticData,dynamicDataExample);
            //     this.nets.push(net);
            //   }
            // })
                      // this.getJSON('assets/densities/net2_den1_python.json').subscribe(dynamicData=> {
                      //   console.log('d', dynamicData);
                      // })
    // })
  }
}
