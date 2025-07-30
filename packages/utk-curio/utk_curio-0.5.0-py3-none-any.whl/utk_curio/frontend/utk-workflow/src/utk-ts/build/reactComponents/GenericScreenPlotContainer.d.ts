import './Dragbox.css';
type GenericScreenPlotProps = {
    id: any;
    disp: boolean;
    x: number;
    y: number;
    svgId: string;
    knotsByPhysical: any;
    activeKnotPhysical: any;
    updateStatus: any;
};
export declare const GenericScreenPlotContainer: ({ id, disp, x, y, svgId, knotsByPhysical, activeKnotPhysical, updateStatus }: GenericScreenPlotProps) => JSX.Element;
export {};
