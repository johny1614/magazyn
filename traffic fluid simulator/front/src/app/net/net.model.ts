import { Optional } from "@angular/core";
export class Point {
    constructor(public x, public y) {
    }
}
export enum Light {
    green, yellow, red, none
}
export class LightPositioned {
    constructor(public light: Light, public position: Point, public imageName: string) { }
}
export class LightsSignalization {
    left: LightPositioned;
    straigth: LightPositioned;
    right: LightPositioned;
}
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
export interface RESTData {
    learningEpochs: number;
    learningMethod: string;
    nets: any[];
}
export interface ILine {
    startPoint: Point;
    endPoint: Point;
    densities?: number[];
    ligths?: LightsSignalization;
    arrowWidth?: number;
}
export class NetFactory {
    static getLine(line: ILine): Line {
        if (line.densities || line.ligths) {
            return new Line(line.startPoint, line.endPoint, line.densities, line.ligths, line.arrowWidth)
        }
        return new Line(line.startPoint, line.endPoint);
    }
    static netFromJson(staticData, dynamicData?): Net {
        const lines = [];
        staticData.lines.forEach(iline => lines.push(NetFactory.getLine(iline)));
        let i = 0;
        if (dynamicData) {
            lines.forEach(line => {
                line.sections.forEach(section => {
                    section.density = dynamicData.densities[i];
                    i++;
                });
            });
        }
        const time = dynamicData ? dynamicData.time : 0;
        return new Net(time, lines);
    }
    static attachDensities(){

    }
}
export class Line {
    constructor(public startPoint: Point, public endPoint: Point, public densities?: number[], public lights?: LightsSignalization, public arrowWidth?: number) {
        this.arrowWidth = this.arrowWidth ? this.arrowWidth : 20;
        const divisions = densities ? densities.length : 1;
        this.a = (endPoint.y - startPoint.y) / (endPoint.x - startPoint.x)
        let x = startPoint.x;
        let y = startPoint.y;
        for (let i = 1; i <= divisions; i++) {
            let old_x = x;
            let old_y = y;
            x = (endPoint.x - startPoint.x) / divisions * i + startPoint.x;
            y = (endPoint.y - startPoint.y) / divisions * i + startPoint.y;
            let section: Section;
            if (densities[i - 1]) {
                section = new Section(new Point(old_x, old_y), new Point(x, y), this.a, densities[i - 1]);
            } else {
                section = new Section(new Point(old_x, old_y), new Point(x, y), this.a);
            }
            this.sections.push(section);
        }
    }
    a: number; // wspolczynnik kierunkowy
    sections: Section[] = [];
}

export class Net {
    constructor(public time: number, public lines: Line[]) { }
}