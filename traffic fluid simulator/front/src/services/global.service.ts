import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GlobalService {
  timeChanger: Subject<number> = new Subject();
  constructor() { }
}
