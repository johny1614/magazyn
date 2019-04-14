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
  dynamicData: any;
  staticData: any;
  timeDisplay;

  constructor(private http: HttpClient,private globaclService: GlobalService) { }
  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }
  increaseTime(){
    this.globaclService.timeChanger.next(1);
  }
  decreaseTime(){
    this.globaclService.timeChanger.next(-1);
  }
  attachDensities(staticData, dynamicData): Net[] {
    const nets: Net[] = [];
    for (let i = 0; i < dynamicData.nets.length; i++) {
      let staticNet;
      staticNet = NetFactory.netFromJson(staticData) // has to be here initialized
      staticNet.time = i;
      let dynamicNet = dynamicData.nets[i];
      let k = 0;
      for (let line of staticNet.lines) {
        let densities = []
        for (let section of line.sections) {
          section.density = dynamicNet.densities[k]
          densities.push(dynamicNet.densities[k]);
          k++;
        }
        line.densities = densities;
      }
      nets.push(staticNet);
    }
    return nets;
  }
  getLight(light: SingleLight, restNet): string {
    let restLight = restNet.lights[light.to - 1][light.from - 1]
    const result = restLight === 1 ? "green" : "red";
    return result;
  }
  lightTheLine(netIndex, line_index, dynamicNet) {
    const line = this.nets[netIndex].lines[line_index]
    const keys = Object.keys(line.lights)
    keys.forEach(key => {
      if (line.lights) {
        line.lights.straigth.imageName = line.lights.straigth.imageName + this.getLight(line.lights.straigth, dynamicNet);
      }
    });
  }
  attachLights(dynamicData) {
    for (let i = 0; i < this.nets.length; i++) {
      for (let line_index = 0; line_index < this.nets[i].lines.length; line_index++) {
        let line: Line = this.nets[i].lines[line_index]
        if (line.lights) {
          this.lightTheLine(i, line_index, dynamicData.nets[i])
        }

      }
    }
  }
  ngOnInit() {
    this.getJSON('assets/nets/net2.json').subscribe(staticData => {
      this.getJSON('assets/densities/net2_den1_python.json').subscribe(dynamicData => {
        this.nets = this.attachDensities(staticData, dynamicData);
        this.attachLights(dynamicData)
      });
    });
  }
}