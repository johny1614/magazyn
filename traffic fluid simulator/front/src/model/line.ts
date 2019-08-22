import { Point } from "./point";
import { LightsSignalization } from "./light";
import { Section } from "./section";

export interface ILine {
    startPoint: Point;
    endPoint: Point;
    densities?: number[];
    ligths?: LightsSignalization;
    arrowWidth?: number;
    x_move?: number;
}
export class Line {
    constructor(public startPoint: Point, public endPoint: Point, public densities?: number[], public lights?: LightsSignalization,public x_move?: number) {
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