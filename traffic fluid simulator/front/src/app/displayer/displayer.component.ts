import { Component, OnInit, Input } from '@angular/core';
import { CanvasService } from '../canvas.service';
import { Net } from 'src/model/net';
import { GlobalService } from 'src/services/global.service';

@Component({
  selector: 'app-displayer',
  templateUrl: './displayer.component.html',
  styleUrls: ['./displayer.component.css'],
  providers: [CanvasService]
})
export class DisplayerComponent implements OnInit {
  @Input()
  nets: Net[];
  timeDisplay: number = 0;

  constructor(private globalService: GlobalService) {
  }

  ngOnInit() {
    this.globalService.timeChanger.subscribe((timeChange) => {
      this.timeDisplay += timeChange;
    });
  }

  logNets() {
    console.log(this.nets);

  }

  roundedRewards() {
    let rewards = []
    this.nets[this.timeDisplay] && this.nets[this.timeDisplay].rewards && 
    this.nets[this.timeDisplay].rewards.forEach(reward => rewards.push(Math.round(reward)));
    return rewards;
  }

}
