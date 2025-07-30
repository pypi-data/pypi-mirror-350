import { ColorHEX } from './constants';
import { IMapStyle } from './interfaces';
export declare class MapStyle {
    protected static default: IMapStyle;
    protected static notFound: ColorHEX;
    protected static highlight: ColorHEX;
    protected static custom: IMapStyle;
    /**
     * Converts from hex colors to rgb colors
     * @param hex
     * @returns
     */
    protected static hexToRgb(hex: ColorHEX): number[];
    /**
     * Get the feature color
     * @param {string} type Feature type
     */
    static getColor(type: keyof IMapStyle): number[];
    /**
     * Set the feature color
     * @param {any} style new map style in id: #rrggbb format
     */
    static setColor(style: string | IMapStyle): Promise<void>;
    static getHighlightColor(): number[];
}
