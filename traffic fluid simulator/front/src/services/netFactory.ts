import {Line, ILine} from 'src/model/line';
import {Net} from 'src/model/net';
import {SingleLight} from 'src/model/light';

export class NetFactory {
  static getLine(line: ILine): Line {
    if (line.densities || line.ligths) {
      return new Line(line.startPoint, line.endPoint, line.densities, line.ligths);
    }
    return new Line(line.startPoint, line.endPoint);
  }

  static netFromJson(staticData, dynamicData?): Net {
    const lines = [];
    const staticLinesCopy = JSON.parse(JSON.stringify(staticData.lines));
    console.log('staticLinesCopy', staticLinesCopy);
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

  static getLight(light: SingleLight, restNet): string {
    let restLight = restNet.lights[light.to][light.from];
    const result = restLight === 0 ? 'red' : 'green';
    return result;
  }

  static removeLightsFromName(imageName) {
    const regs = ['_red', '_orange', '_green'];
    for (const reg of regs) {
      imageName = imageName.replace(reg, '');
    }
    return imageName;
  }

  static lightTheSignalization(nets, netIndex, line_index, dynamicNet) {
    const line = nets[netIndex].lines[line_index];
    const keys = Object.keys(line.lights);
    keys.forEach(key => {
      if (line.lights.straight) {
        line.lights.straight.imageName = this.removeLightsFromName(line.lights.straight.imageName);
        line.lights.straight.imageName = line.lights.straight.imageName + '_' + NetFactory.getLight(line.lights.straight, dynamicNet);
      }
      if (line.lights.right) {
        line.lights.right.imageName = this.removeLightsFromName(line.lights.right.imageName);
        line.lights.right.imageName = line.lights.right.imageName + '_' + NetFactory.getLight(line.lights.right, dynamicNet);
      }
      if (line.lights.left) {
        line.lights.left.imageName = this.removeLightsFromName(line.lights.left.imageName);
        line.lights.left.imageName = line.lights.left.imageName + '_' + NetFactory.getLight(line.lights.left, dynamicNet);
      }
    });
  }

  static attachLights(nets, dynamicData) {
    for (let i = 0; i < nets.length; i++) {
      for (let line_index = 0; line_index < nets[i].lines.length; line_index++) {
        const line: Line = nets[i].lines[line_index];
        if (line.lights) {
          NetFactory.lightTheSignalization(nets, i, line_index, dynamicData.nets[i]);
        }
      }
    }
  }

  static getNetsWithDensity(staticData, dynamicData): Net[] {
    const nets: Net[] = [];
    for (let i = 0; i < dynamicData.nets.length; i++) {
      let staticNet;
      staticNet = NetFactory.netFromJson(staticData); // has to be here initialized
      staticNet.time = i;
      let dynamicNet = dynamicData.nets[i];
      let k = 0;
      for (let line of staticNet.lines) {
        let densities = [];
        for (let section of line.sections) {
          section.density = Math.round(dynamicNet.densities[k] * 10) / 10;
          densities.push(section.density);
          k++;
        }
        line.densities = densities;
      }
      nets.push(staticNet);
    }
    return nets;
  }
}
