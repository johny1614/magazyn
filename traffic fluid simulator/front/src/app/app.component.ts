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
  title: string = 'app';
  nets: Net[] = [];
  load_name: string;
  load_text: string;
  is_loaded_right: boolean;

  constructor(private http: HttpClient, private globaclService: GlobalService) {
  }

  public getJSON(url): Observable<any> {
    return this.http.get(url);
  }

  increaseTime() {
    this.globaclService.timeChanger.next(1);
  }

  decreaseTime() {
    this.globaclService.timeChanger.next(-1);
  }

  ngOnInit(){
    this.load_name='netpolibuda_x'
    this.load();
  }


  load() {
    // 'net11_learnt_0'
    console.log(this.load_name)
    const first_occurance = this.load_name.indexOf('_');
    const net_name = this.load_name.substring(0, first_occurance);
    const den_name = this.load_name.substring(first_occurance + 1, 999);
    console.log('den name',den_name)
    this.getJSON('assets/nets/' + net_name + '.json').subscribe(staticData => {
      this.nets = [NetFactory.netFromJson(staticData)];
      let net = 'assets/densities/' + net_name + '_' + den_name + '.json';
      this.getJSON(net).subscribe(dynamicData => {
        this.nets = NetFactory.getNetsWithDensity(staticData, dynamicData);
        NetFactory.attachLights(this.nets, dynamicData);
        NetFactory.attachRewards(this.nets, dynamicData)
        NetFactory.attachActions(this.nets, dynamicData)
        NetFactory.attachA(this.nets, dynamicData);
        this.load_text = 'Wczytanie się powiodło'
        this.is_loaded_right = true;
      },
        error => {
          this.load_text = 'Wczytanie się nie powiodło'
          this.is_loaded_right = false;
        });
    },
      error => {
        this.load_text = 'Wczytanie się nie powiodło'
        this.is_loaded_right = false;
      });

  }
}
