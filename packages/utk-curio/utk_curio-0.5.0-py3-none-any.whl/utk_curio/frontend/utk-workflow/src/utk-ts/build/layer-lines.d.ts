import { OperationType, LevelType } from "./constants";
import { ILayerData, ILayerFeature, IKnot, IExKnot } from "./interfaces";
import { Layer } from "./layer";
import { Shader } from "./shader";
import { AuxiliaryShader } from "./auxiliaryShader";
export declare class LinesLayer extends Layer {
    protected _zOrder: number;
    protected _coordsByCOORDINATES: number[][];
    protected _coordsByCOORDINATES3D: number[][];
    protected _coordsByOBJECTS: number[][];
    protected _highlightByCOORDINATES: boolean[][];
    protected _highlightByCOORDINATES3D: boolean[][];
    protected _highlightByOBJECTS: boolean[][];
    constructor(info: ILayerData, dimensions: number | undefined, order: number | undefined, geometryData: ILayerFeature[]);
    supportInteraction(eventName: string): boolean;
    updateMeshGeometry(data: ILayerFeature[]): void;
    getSelectedFiltering(): number[] | null;
    updateShaders(shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    directAddMeshFunction(functionValues: number[][], knotId: string): void;
    updateFunction(knot: IKnot | IExKnot, shaders: (Shader | AuxiliaryShader)[]): void;
    distributeFunctionValues(functionValues: number[][] | null): number[][] | null;
    innerAggFunc(functionValues: number[] | null, startLevel: LevelType, endLevel: LevelType, operation: OperationType): number[] | null;
    setHighlightElements(elements: number[], level: LevelType, value: boolean, shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    getFunctionValueIndexOfId(id: number, level: LevelType): number | null;
    getCoordsByLevel(level: LevelType, centroid: number[] | Float32Array | undefined, viewId: number): number[][];
    getFunctionByLevel(level: LevelType, knotId: string): number[][][];
    getHighlightsByLevel(level: LevelType): boolean[];
    /**
     * Layer render function signature
     * @param {WebGL2RenderingContext} glContext WebGL context
     */
    render(glContext: WebGL2RenderingContext, shaders: (Shader | AuxiliaryShader)[]): void;
}
