import { Component, OnInit, Input } from '@angular/core';
import { CanvasService } from '../canvas.service';
import { Net } from 'src/model/net';

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

  constructor() { }

  ngOnInit() {
  }

}
