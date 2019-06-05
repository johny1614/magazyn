import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Net } from 'src/model/net';
import { SingleLight } from 'src/model/light';
import { Line } from 'src/model/line';
import { NetFactory } from 'src/services/netFactory';
import { GlobalService } from 'src/services/global.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  nets: Net[] = [];

  constructor(private http: HttpClient, private globaclService: GlobalService) {
  }

  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  // asdsad

  increaseTime() {
    this.globaclService.timeChanger.next(1);
  }

  decreaseTime() {
    this.globaclService.timeChanger.next(-1);
  }

  ngOnInit() {
    this.getJSON('assets/nets/net4.json').subscribe(staticData => {
      this.nets = [NetFactory.netFromJson(staticData)];
      this.getJSON('assets/densities/net4_last_epoch.json').subscribe(dynamicData => {
        console.log('jest dynamicData', dynamicData);
        this.nets = NetFactory.getNetsWithDensity(staticData, dynamicData);
        NetFactory.attachLights(this.nets, dynamicData);
        NetFactory.attachRewards(this.nets, dynamicData)
        NetFactory.attachActions(this.nets, dynamicData)
        NetFactory.attachA(this.nets, dynamicData);
        console.log('this.nets',this.nets)
      });
    });

  }
}
