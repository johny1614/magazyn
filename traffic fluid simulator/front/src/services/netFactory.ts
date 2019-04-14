import { Line, ILine } from "src/model/line";
import { Net } from "src/model/net";

export class NetFactory {
    static getLine(line: ILine): Line {
        if (line.densities || line.ligths) {
            return new Line(line.startPoint, line.endPoint, line.densities, line.ligths, line.arrowWidth)
        }
        return new Line(line.startPoint, line.endPoint);
    }
    static netFromJson(staticData, dynamicData?): Net {
        const lines = [];
        const staticLinesCopy=JSON.parse(JSON.stringify(staticData.lines))
        staticLinesCopy.forEach(iline => lines.push(NetFactory.getLine(iline)));
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
}