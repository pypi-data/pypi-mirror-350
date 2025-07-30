import { OperationType, LevelType } from "./constants";
import { IExKnot, IKnot, ILayerData, ILayerFeature } from "./interfaces";
import { Layer } from "./layer";
import { AuxiliaryShader } from "./auxiliaryShader";
import { Shader } from "./shader";
export declare class BuildingsLayer extends Layer {
    protected _zOrder: number;
    protected _coordsByCOORDINATES: number[][];
    protected _coordsByCOORDINATES3D: number[][];
    protected _coordsByOBJECTS: number[][];
    protected _highlightByCOORDINATES: boolean[][];
    protected _highlightByCOORDINATES3D: boolean[][];
    protected _highlightByOBJECTS: boolean[][];
    constructor(info: ILayerData, zOrder: number | undefined, geometryData: ILayerFeature[]);
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
    applyTexSelectedCells(glContext: WebGL2RenderingContext, spec: any, specType: string, shaders: (Shader | AuxiliaryShader)[]): Promise<void>;
    clearAbsSurface(shaders: (Shader | AuxiliaryShader)[]): void;
    createFootprintPlot(glContext: WebGL2RenderingContext, x: number, y: number, update: boolean, shaders: (Shader | AuxiliaryShader)[]): void;
    applyFootprintPlot(glContext: WebGL2RenderingContext, spec: any, plotNumber: number, specType: string, shaders: (Shader | AuxiliaryShader)[]): Promise<number | undefined>;
    updateFootprintPlot(glContext: WebGL2RenderingContext, d3Expec: any, plotNumber: number, deltaHeight: number, specType: string, shaders: (Shader | AuxiliaryShader)[]): Promise<void>;
    perFaceAvg(functionValues: number[][], indices: number[], ids: number[]): number[][];
    /**
     * Distributes triangle avg to the coordinates that composes the triangle.
     * The coordinates need to be duplicated, meaning that there are unique indices.
     */
    perCoordinatesAvg(avg_accumulation_triangle: number[][], coordsLength: number, indices: number[]): number[][];
    distributeFunctionValues(functionValues: number[][] | null): number[][] | null;
    innerAggFunc(functionValues: number[] | null, startLevel: LevelType, endLevel: LevelType, operation: OperationType): number[] | null;
    getFunctionValueIndexOfId(id: number, level: LevelType): number | null;
    getCoordsByLevel(level: LevelType, centroid: number[] | Float32Array | undefined, viewId: number): number[][];
    getFunctionByLevel(level: LevelType, knotId: string): number[][][];
    getHighlightsByLevel(level: LevelType, shaders: (Shader | AuxiliaryShader)[]): boolean[];
    getIdLastHighlightedBuilding(shaders: (Shader | AuxiliaryShader)[]): number[] | undefined;
    highlightBuilding(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[]): void;
    highlightBuildingsInArea(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[], radius: number): void;
}
