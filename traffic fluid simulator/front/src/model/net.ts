import {Line} from './line';

export class Net {
  A: any;
  constructor(public time: number, public lines: Line[]) {
  }
}
