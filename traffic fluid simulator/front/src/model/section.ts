import { Point } from "./point";

export class Section {
    constructor(
        public startPoint: Point,
        public endPoint: Point,
        public a: number,
        public density?: number
    ) {
        this.middlePoint = new Point((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2);
    }
    middlePoint: Point;
}