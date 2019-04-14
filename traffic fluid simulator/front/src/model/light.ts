import { Point } from "./point";

export enum Light {
    green, yellow, red, none
}
export interface SingleLight {
    light: Light;
    position: Point;
    imageName: string;
    from: number; // section number
    to: number; // section number
}
export class LightsSignalization {
    left?: SingleLight;
    straigth?: SingleLight;
    right?: SingleLight;
}