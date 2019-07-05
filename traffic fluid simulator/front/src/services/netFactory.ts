import { Line, ILine } from 'src/model/line';
import { Net } from 'src/model/net';
import { SingleLight } from 'src/model/light';

export class NetFactory {
  static getLine(line: ILine): Line {
    if (line.densities || line.ligths) {
      return new Line(line.startPoint, line.endPoint, line.densities, line.ligths);
    }
    return new Line(line.startPoint, line.endPoint);
  }

  static attachA(nets: Net[], dynamicData) {
    for (let i = 0; i < nets.length; i++) {
      nets[i].A = dynamicData.nets[i].lights;
    }
  }

  static netFromJson(staticData, dynamicData?): Net {
    const lines = [];
    const staticLinesCopy = JSON.parse(JSON.stringify(staticData.lines));
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
  // static getLightNormalNet(line,){
  //   let restLight = restNet.lights[light.to][light.from];
  //   const result = restLight === 0 ? 'red' : 'green';
  //   return result;
  // }

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
        console.log('po ', line.lights.straight.imageName)
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

  static changeLights(net): Net {
    for (let line of net.lines) {
      // console.log('przed ', line.lights.straight.imageName)
      if (net.lights) {
        if (line.lights.straight) {
          line.lights.straight.imageName = this.removeLightsFromName(line.lights.straight.imageName);
          let actual_light = net.A[line.lights.straight.to][line.lights.straight.from] > 0 ? 'green' : 'red';
          line.lights.straight.imageName = line.lights.straight.imageName + '_' + actual_light
          if (actual_light=='green'){
            console.log('linia zielona!',line)
          }
        }
        if (line.lights.right) {
          line.lights.right.imageName = this.removeLightsFromName(line.lights.right.imageName);
          let actual_light = net.A[line.lights.right.to][line.lights.right.from] > 0 ? 'green' : 'red';
          line.lights.right.imageName = line.lights.right.imageName + '_' + actual_light
          console.log('linia zielona!',line)

        }
        if (line.lights.left) {
          line.lights.left.imageName = this.removeLightsFromName(line.lights.left.imageName);
          let actual_light = net.A[line.lights.left.to][line.lights.left.from] > 0 ? 'green' : 'red';
          line.lights.left.imageName = line.lights.left.imageName + '_' + actual_light
          console.log('linia zielona!',line)

          // line.lights.left.imageName = line.lights.left.imageName + '_' + NetFactory.getLight(line.lights.left, dynamicNet);
        }
      }
    }
    return net
  }

  static attachLights(nets, dynamicData) {
    console.log('nets', nets);
    console.log('nets lenf',nets.length)
    for (let net_index = 0; net_index < nets.length; net_index++) {
      console.log('net_index', net_index);
      console.log('A', dynamicData.nets[net_index].lights)
      for (let line_index = 0; line_index < nets[net_index].lines.length; line_index++) {
        const line: Line = nets[net_index].lines[line_index];
        if (line.lights) {
          NetFactory.lightTheSignalization(nets, net_index, line_index, dynamicData.nets[net_index]);
        }
      }
    }
  }

  static attachRewards(nets, dynamicData) {
    console.log(dynamicData)
    for (let i = 0; i < nets.length; i++) {
      let net = nets[i]
      net.rewards = dynamicData.nets[i].rewards
    }
  }
  static attachActions(nets, dynamicData) {
    for (let i = 0; i < nets.length; i++) {
      let net = nets[i]
      net.actions = dynamicData.nets[i].actions
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
