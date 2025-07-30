import { Shader } from './shader';
import { Mesh } from "./mesh";
import { ILayerFeature, IMapStyle, IJoinedLayer, IJoinedObjects, IKnot, IJoinedJson, IExternalJoinedJson, IExKnot } from './interfaces';
import { LayerType, RenderStyle, OperationType, LevelType } from './constants';
import { AuxiliaryShader } from './auxiliaryShader';
export declare abstract class Layer {
    protected _id: string;
    protected _type: LayerType;
    protected _styleKey: keyof IMapStyle;
    protected _renderStyle: RenderStyle[];
    protected _joinedLayers: IJoinedLayer[];
    protected _joinedObjects: IJoinedObjects[];
    protected _externalJoinedJson: IExternalJoinedJson;
    protected _camera: any;
    protected _mesh: Mesh;
    constructor(id: string, type: LayerType, styleKey: keyof IMapStyle, renderStyle: RenderStyle[] | undefined, dimension: number, zOrder: number);
    setJoinedJson(joinedJson: IJoinedJson | IExternalJoinedJson): void;
    /**
     * Accessor for the layer id
     */
    get id(): string;
    /**
     * Accessor for the layer style
     */
    get style(): keyof IMapStyle;
    get joinedLayers(): IJoinedLayer[];
    get externalJoinedJson(): IExternalJoinedJson;
    get joinedObjects(): IJoinedObjects[];
    /**
     * Sends the camera to the layer
     */
    set camera(camera: any);
    get mesh(): Mesh;
    set mesh(mesh: Mesh);
    get renderStyle(): RenderStyle[];
    /**
     * Data update signature
     */
    abstract updateMeshGeometry(data: ILayerFeature[]): void;
    abstract updateShaders(shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array, viewId: number): void;
    abstract updateFunction(knot: IKnot | IExKnot, shaders: (Shader | AuxiliaryShader)[]): void;
    abstract render(glContext: WebGL2RenderingContext, shaders: (Shader | AuxiliaryShader)[]): void;
    /**
     * Distributes the function values inside the layer according to its semantics so it can be rendered. (i.e. function values of coordinates in building cells are averaged)
     * This function is called as the last step of the rendering pipeline (after all the joins and operations with the abstract data)
     * @param functionValues function values per coordinate per timestep
     */
    abstract distributeFunctionValues(functionValues: number[][] | null): number[][] | null;
    /**
     * Aggregates the function values to a more coarse level
     * @param functionValues function values per coordinate (but all the coordinates that compose a basic struct at the start level have the same values). If the start level is building, for instance, all coordinates of a specific building have the same value.
     *
     */
    abstract innerAggFunc(functionValues: number[] | null, startLevel: LevelType, endLevel: LevelType, operation: OperationType): number[] | null;
    /**
     * Given the id of an element that is in a specific level, returns the function value index that should be used to
     * retrieve the representative function value of that element
     */
    abstract getFunctionValueIndexOfId(id: number, level: LevelType): number | null;
    abstract getCoordsByLevel(level: LevelType, centroid: number[] | Float32Array, viewId: number): number[][];
    abstract getFunctionByLevel(level: LevelType, knotId: string): number[][][];
    abstract getHighlightsByLevel(level: LevelType, shaders: (Shader | AuxiliaryShader)[]): boolean[];
    abstract supportInteraction(eventName: string): boolean;
    /**
     *
     * @param elements array of elements indices (follow the order they appear in the layer json file)
     */
    abstract setHighlightElements(elements: number[], level: LevelType, value: boolean, shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array, viewId: number): void;
    abstract directAddMeshFunction(functionValues: number[][], knotId: string): void;
    abstract getSelectedFiltering(shaders: (Shader | AuxiliaryShader)[]): number[] | null;
}
