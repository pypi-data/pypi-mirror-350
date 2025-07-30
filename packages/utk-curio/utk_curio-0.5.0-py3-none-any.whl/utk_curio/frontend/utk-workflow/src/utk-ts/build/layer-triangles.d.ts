import { OperationType, LevelType } from "./constants";
import { ILayerData, ILayerFeature, IKnot, IExKnot } from "./interfaces";
import { Layer } from "./layer";
import { AuxiliaryShader } from "./auxiliaryShader";
import { Shader } from "./shader";
export declare class TrianglesLayer extends Layer {
    protected _zOrder: number;
    protected _dimensions: number;
    protected _coordsByCOORDINATES: number[][];
    protected _coordsByCOORDINATES3D: number[][];
    protected _coordsByOBJECTS: number[][];
    protected _highlightByCOORDINATES: boolean[][];
    protected _highlightByCOORDINATES3D: boolean[][];
    protected _highlightByOBJECTS: boolean[][];
    constructor(info: ILayerData, dimensions: number | undefined, zOrder: number | undefined, geometryData: ILayerFeature[]);
    supportInteraction(eventName: string): boolean;
    updateMeshGeometry(data: ILayerFeature[]): void;
    updateShaders(shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    directAddMeshFunction(functionValues: number[][], knotId: string): void;
    updateFunction(knot: IKnot | IExKnot, shaders: (Shader | AuxiliaryShader)[]): void;
    setHighlightElements(elements: number[], level: LevelType, value: boolean, shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    getSelectedFiltering(shaders: (Shader | AuxiliaryShader)[]): number[] | null;
    /**
     * Layer render function signature
     * @param {WebGL2RenderingContext} glContext WebGL context
     */
    render(glContext: WebGL2RenderingContext, shaders: (Shader | AuxiliaryShader)[]): void;
    highlightElement(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[]): void;
    highlightElementsInArea(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[], radius: number): void;
    getIdLastHighlightedElement(shaders: (Shader | AuxiliaryShader)[]): number[] | undefined;
    distributeFunctionValues(functionValues: number[][] | null): number[][] | null;
    innerAggFunc(functionValues: number[] | null, startLevel: LevelType, endLevel: LevelType, operation: OperationType): number[] | null;
    getFunctionValueIndexOfId(id: number, level: LevelType): number | null;
    /**
     *
     * @returns each position of the array contains an element of that level
     */
    getCoordsByLevel(level: LevelType, centroid: number[] | Float32Array | undefined, viewId: number): number[][];
    getFunctionByLevel(level: LevelType, knotId: string): number[][][];
    getHighlightsByLevel(level: LevelType): boolean[];
}
