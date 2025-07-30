import { IExKnot, IKnot } from "./interfaces";
import { Knot } from "./knot";
import { Layer } from "./layer";
export declare class KnotManager {
    protected _knots: Knot[];
    protected _updateStatusCallback: any;
    init(updateStatusCallback: any): void;
    get knots(): Knot[];
    createKnot(id: string, physicalLayer: Layer, knotSpecification: IKnot | IExKnot, grammarInterpreter: any, visible: boolean): Knot;
    toggleKnot(id: string, value?: boolean | null): void;
    overwriteSelectedElements(externalSelected: number[], layerId: string, viewId: number): void;
    getKnotById(knotId: string): Knot | null;
}
