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
    this.getJSON('assets/nets/net11.json').subscribe(staticData => {
      console.log('static jest',staticData)
      this.nets = [NetFactory.netFromJson(staticData)];
      // let net = 'assets/densities/net4_sequential.json'
      // let net = 'assets/densities/net11_den_843015.json';
      // let net = 'assets/densities/net11_den_083311.json';
      // let net = 'assets/densities/net11_den_0006321.json';
      let net = 'assets/densities/net11_den_000602.json';

      // let net = 'assets/densities/net11_den_phase_0_1_yellow_purple.json';
      // let net = 'assets/densities/net4_0_1_2_yellow_phase.json';
      // let net = 'assets/densities/net4_0_1_2_yellow_phase.json';

      // let net = 'assets/densities/net4_cross.json'
      // let net = 'assets/densities/net4_base_zeros.json';
      // let net = 'assets/densities/net4_last_epoch.json'
      // let net = 'assets/densities/net4_learnt-10.json';
      // waaat
      // let net = 'assets/densities/net1_den1.json';
      // let net = 'assets/densities/net4_test_no_5.json';
      // let net = 'assets/densities/net4_test_no_2.json';
      // let net = 'assets/densities/net4_seq.json';
      // let net = 'assets/densities/net5_random_0.json';
      // let net = 'assets/densities/net4_random_3.json';
      // let net = 'assets/densities/net4_stan_monitorowany_3.json';
      // let net = 'assets/densities/net4_learnt-3.json';
      this.getJSON(net).subscribe(dynamicData => {
        // asdsa
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
