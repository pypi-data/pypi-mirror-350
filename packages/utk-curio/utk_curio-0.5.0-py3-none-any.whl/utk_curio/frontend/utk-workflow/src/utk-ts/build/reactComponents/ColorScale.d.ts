import './Dragbox.css';
type ColorScaleProps = {
    id: any;
    x: number;
    y: number;
    range: number[];
    domain: number[];
    cmap: string;
    scale: string;
    disp: boolean;
    keyValue: number;
};
export declare const ColorScaleContainer: ({ id, x, y, range, domain, cmap, scale, disp, keyValue }: ColorScaleProps) => JSX.Element;
export {};
