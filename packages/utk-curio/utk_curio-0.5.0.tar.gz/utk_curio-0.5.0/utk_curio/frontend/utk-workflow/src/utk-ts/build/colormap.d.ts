export declare abstract class ColorMap {
    protected static interpolator: (t: number) => string;
    static getColor(value: number, color: string): number[];
    static getColorMap(color: string, res?: number): number[];
}
