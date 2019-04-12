import { Optional } from "@angular/core";

export enum Light {
    green, yellow, red, none
}
export class LightPositioned{
    constructor(public light: Light, public position: Point,public imageName: string){}
}
export class LightsSignalization {
    left: LightPositioned;
    straigth: LightPositioned;
    right: LightPositioned;
}
export class Point {
    constructor(public x, public y) {
    }
}
export class Section {
    constructor(
        public startPoint: Point,
        public endPoint: Point,
        public a: number,
        public density: number
    ) {
        this.middlePoint = new Point((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2);
    }
    middlePoint: Point;

}
export class Line {
    constructor(public startPoint: Point, public endPoint: Point, public densities: number[], public lights?: LightsSignalization) {
        const divisions = densities.length;
        console.log('densities', densities);
        this.a = (endPoint.y - startPoint.y) / (endPoint.x - startPoint.x)
        let x = startPoint.x;
        let y = startPoint.y;
        for (let i = 1; i <= divisions; i++) {
            let old_x = x;
            let old_y = y;
            x = (endPoint.x - startPoint.x) / divisions * i + startPoint.x;
            y = (endPoint.y - startPoint.y) / divisions * i + startPoint.y;
            console.log('den', densities[i - 1])
            const section = new Section(new Point(old_x, old_y), new Point(x, y), this.a, densities[i - 1]);
            this.sections.push(section);
        }
    }
    a: number; // wspolczynnik kierunkowy
    sections: Section[] = [];
}
export class Net {
    lines: Line[];
}