import {Line} from './line';

export class Net {
  A: any;
  rewards: number[];
  actions: number[];
  constructor(public time: number, public lines: Line[]) {
  }
}
