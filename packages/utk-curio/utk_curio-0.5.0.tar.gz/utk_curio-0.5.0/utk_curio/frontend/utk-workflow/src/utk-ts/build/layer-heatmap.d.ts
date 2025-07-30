import { OperationType, LevelType } from "./constants";
import { ILayerData, ILayerFeature, IKnot, IExKnot } from "./interfaces";
import { Layer } from "./layer";
import { AuxiliaryShader } from './auxiliaryShader';
import { Shader } from './shader';
export declare class HeatmapLayer extends Layer {
    protected _zOrder: number;
    protected _dimensions: number;
    protected _coordsByCOORDINATES: number[][];
    protected _coordsByCOORDINATES3D: number[][];
    protected _coordsByOBJECTS: number[][];
    protected _highlightByCOORDINATES: boolean[][];
    protected _highlightByCOORDINATES3D: boolean[][];
    protected _highlightByOBJECTS: boolean[][];
    constructor(info: ILayerData, zOrder: number | undefined, geometryData: ILayerFeature[]);
    updateMeshGeometry(data: ILayerFeature[]): void;
    updateShaders(shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    directAddMeshFunction(functionValues: number[][], knotId: string): void;
    getSelectedFiltering(): number[] | null;
    updateFunction(knot: IKnot | IExKnot, shaders: (Shader | AuxiliaryShader)[]): void;
    supportInteraction(interaction: string): boolean;
    setHighlightElements(elements: number[], level: LevelType, value: boolean, shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    render(glContext: WebGL2RenderingContext, shaders: (Shader | AuxiliaryShader)[]): void;
    perFaceAvg(functionValues: number[][], indices: number[], ids: number[]): number[][];
    /**
     * Distributes triangle avg to the coordinates that composes the triangle.
     * The coordinates need to be duplicated, meaning that there are unique indices.
     */
    perCoordinatesAvg(avg_accumulation_triangle: number[][], coordsLength: number, indices: number[]): number[][];
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
