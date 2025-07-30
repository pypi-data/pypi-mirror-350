import { vec2, vec3, mat4 } from 'gl-matrix';
import { Root } from 'react-dom/client';

/**
 * Layer types definition
 */
declare enum LayerType {
    POINTS_LAYER = "POINTS_LAYER",
    LINES_2D_LAYER = "LINES_2D_LAYER",
    LINES_3D_LAYER = "LINES_3D_LAYER",
    TRIANGLES_2D_LAYER = "TRIANGLES_2D_LAYER",
    TRIANGLES_3D_LAYER = "TRIANGLES_3D_LAYER",
    BUILDINGS_LAYER = "BUILDINGS_LAYER",
    HEATMAP_LAYER = "HEATMAP_LAYER"
}
/**
 * Render styles definition
 */
declare enum RenderStyle {
    FLAT_COLOR = "FLAT_COLOR",
    FLAT_COLOR_MAP = "FLAT_COLOR_MAP",
    FLAT_COLOR_POINTS = "FLAT_COLOR_POINTS",
    FLAT_COLOR_POINTS_MAP = "FLAT_COLOR_POINTS_MAP",
    SMOOTH_COLOR = "SMOOTH_COLOR",
    SMOOTH_COLOR_MAP = "SMOOTH_COLOR_MAP",
    SMOOTH_COLOR_MAP_TEX = "SMOOTH_COLOR_MAP_TEX",
    PICKING = "PICKING",
    ABSTRACT_SURFACES = "ABSTRACT_SURFACES",
    OUTLINE = "OUTLINE",
    COLOR_POINTS = "COLOR_POINTS"
}
/**
 * Supported aggregations for layer linking
 */
declare enum OperationType {
    MAX = "MAX",
    MIN = "MIN",
    AVG = "AVG",
    SUM = "SUM",
    COUNT = "COUNT",
    NONE = "NONE",
    DISCARD = "DISCARD"
}
declare enum ViewArrangementType {
    LINKED = "LINKED",
    EMBEDDED = "EMBEDDED"
}
declare enum PlotArrangementType {
    SUR_EMBEDDED = "SUR_EMBEDDED",
    FOOT_EMBEDDED = "FOOT_EMBEDDED",
    LINKED = "LINKED"
}
declare enum GrammarType {
    PLOT = "PLOT",
    MAP = "MAP",
    MASTER = "MASTER"
}
declare enum SpatialRelationType {
    INTERSECTS = "INTERSECTS",
    CONTAINS = "CONTAINS",
    WITHIN = "WITHIN",
    TOUCHES = "TOUCHES",
    CROSSES = "CROSSES",
    OVERLAPS = "OVERLAPS",
    NEAREST = "NEAREST",
    DIRECT = "DIRECT",
    INNERAGG = "INNERAGG"
}
declare enum LevelType {
    COORDINATES = "COORDINATES",
    OBJECTS = "OBJECTS",
    COORDINATES3D = "COORDINATES3D"
}
declare enum InteractionType {
    BRUSHING = "BRUSHING",
    PICKING = "PICKING",
    AREA_PICKING = "AREA_PICKING",
    NONE = "NONE"
}
declare enum PlotInteractionType {
    CLICK = "CLICK",
    HOVER = "HOVER",
    BRUSH = "BRUSH"
}
declare enum InteractionEffectType {
    FILTER = "FILTER",
    HIGHLIGHT = "HIGHLIGHT"
}
declare enum ComponentIdentifier {
    MAP = "MAP",
    GRAMMAR = "GRAMMAR",
    PLOT = "PLOT"
}
declare enum WidgetType {
    TOGGLE_KNOT = "TOGGLE_KNOT",
    SEARCH = "SEARCH",
    HIDE_GRAMMAR = "HIDE_GRAMMAR"
}
/**
 * Mapview interaction status
 */
declare class MapViewStatu {
    static IDLE: number;
    static DRAG: number;
    static DRAG_RIGHT: number;
}
/**
 * Color type definition
 */
type ColorHEX = `#${string}`;

/**
 * Interface for master grammar
 */
interface IMasterGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    components: (IComponent)[];
    knots: IKnot[];
    ex_knots?: IExKnot[];
    grid: IGrid;
    grammar: boolean;
    grammar_position?: IComponentPosition;
}
interface IExKnot {
    id: string;
    out_name: string;
    in_name?: string;
    group?: IKnotGroup;
    color_map?: string | IConditionBlock;
    range?: number[];
    domain?: number[];
    scale?: string;
}
/**
 * Interface for map grammar
 */
interface IMapGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    camera: ICameraData;
    knots: (string | IConditionBlock)[];
    interactions: (InteractionType | IConditionBlock)[];
    plot: {
        id: string;
    };
    filterKnots?: (number | IConditionBlock)[];
    knotVisibility?: IKnotVisibility[];
    widgets?: IGenericWidget[];
    grammar_type: GrammarType;
}
interface IExternalJoinedJson {
    id: string;
    incomingId: string[];
    inValues: number[][][];
}
/**
 * Interface for plot grammar
 */
interface IPlotGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    name: string;
    plot: any;
    arrangement: string;
    knots: string[];
    interaction: string;
    args?: IPlotArgs;
    interaction_effect?: InteractionEffectType;
    grammar_type: GrammarType;
}
interface IComponent {
    id: string;
    position: IComponentPosition;
}
interface IGrid {
    width: number;
    height: number;
}
interface IGenericWidget {
    type: WidgetType;
    args?: {
        categories: ICategory[];
    };
}
interface ICategory {
    category_name: string;
    elements: (string | ICategory)[];
}
interface IComponentPosition {
    width: number[];
    height: number[];
}
interface IPlotArgs {
    bins?: number | IConditionBlock;
}
interface IKnot {
    id: string;
    group?: IKnotGroup;
    knot_op?: boolean;
    color_map?: string | IConditionBlock;
    integration_scheme: ILinkDescription[];
    range?: number[];
    domain?: number[];
    scale?: string;
}
interface IKnotGroup {
    group_name: string;
    position: number;
}
interface ILinkDescription {
    spatial_relation?: SpatialRelationType;
    out: {
        name: string;
        level: LevelType;
    };
    in?: {
        name: string;
        level: LevelType;
    };
    operation: OperationType | IConditionBlock;
    abstract?: boolean;
    op?: string;
    maxDistance?: number;
    defaultValue?: number;
}
/**
 * Interface with the camera definition
 */
interface ICameraData {
    position: number[];
    direction: {
        right: number[];
        lookAt: number[];
        up: number[];
    };
}
/**
 * Interface with the layer style definition
 */
interface IMapStyle {
    land: ColorHEX;
    roads: ColorHEX;
    parks: ColorHEX;
    water: ColorHEX;
    sky: ColorHEX;
    surface: ColorHEX;
    building: ColorHEX;
}
/**
 * Interface with the layer definition (Feature collection)
 */
interface ILayerData {
    id: string;
    type: LayerType;
    styleKey: keyof IMapStyle;
    data?: ILayerFeature[];
    renderStyle?: RenderStyle[];
}
interface IJoinedJson {
    joinedLayers: IJoinedLayer[];
    joinedObjects: IJoinedObjects[];
}
interface IJoinedObjects {
    joinedLayerIndex: number;
    inValues?: number[] | number[][];
    inIds?: number[][];
}
interface IJoinedLayer {
    spatial_relation: string;
    layerId: string;
    outLevel: string;
    inLevel: string;
    abstract: boolean;
}
/**
 * Interface with the Layer Feature definition (Feature: Geometry collection)
 */
interface ILayerFeature {
    geometry: IFeatureGeometry;
    highlight?: boolean;
    highlightIds?: number[];
}
/**
 * Interface with the feature geometry definition (Geometry: Geometric info)
 */
interface IFeatureGeometry {
    coordinates: number[];
    normals?: number[];
    function?: number[][];
    indices?: number[];
    ids?: number[];
    heights?: number[];
    minHeights?: number[];
    orientedEnvelope?: number[][];
    sectionFootprint?: number[][];
    uv?: number[];
    width?: number[];
    pointsPerSection?: number[];
    discardFuncInterval?: number[];
    varyOpByFunc?: number;
}
interface IConditionBlock {
    condition: IConditionElement[];
}
interface IConditionElement {
    test?: string;
    value: any;
}
interface IKnotVisibility {
    knot: string;
    test: string;
}

/**
 * Half-Edge mesh component
 */
declare class MeshComponent {
    dimension: number;
    coordinates: number[];
    normals: number[];
    functions: {
        "knot": string;
        "timesteps": number[][];
    }[];
    ids: number[];
    heights: number[];
    minHeights: number[];
    orientedEnvelope: number[][];
    sectionFootprint: number[][];
    uv: number[];
    width: number[];
    heightInSection: number[];
    sectionHeight: number[];
    pointsPerSection: number[];
    discardFuncInterval: number[];
    varyOpByFunc: number;
    vertHe: number[];
    vTable: number[];
    oTable: number[];
    constructor(dimension: number);
    nVertex(): number;
    nHalfEdge(): number;
    nTriangle(): number;
    trig(he: number): number;
    next(he: number): number;
    prev(he: number): number;
}
declare class Mesh {
    protected _dimension: number;
    protected _zOrder: number;
    protected _components: MeshComponent[];
    protected _allCoordinates: any;
    protected _allIds: number[];
    protected _allIndices: number[];
    protected _allNormals: number[];
    protected _allFunctions: number[];
    protected _filtered: number[];
    /**
     * Mesh default constructor
     * @param dimension number of dimensions of the input vertices
     */
    constructor(dimension?: number, zOrder?: number);
    /**
     * Get the dimension of the vertices
     */
    get dimension(): number;
    get filtered(): number[];
    /**
     * Converts the local component id to the global mesh id
     * @param cId Component Id
     * @param vId Vertex component Id
     */
    vMeshId(cId: number, vId: number): number;
    /**
     * Converts the global mesh id to the local component id
     * @param vId Vertex mesh Id
     */
    vCompId(vId: number): [number, number];
    /**
     * Converts the local component id to the global mesh id
     * @param cId Component Id
     * @param vId Vertex component Id
     */
    hMeshId(comp: number, heId: number): number;
    /**
     * Converts the global mesh id to the local component id
     * @param hId Vertex mesh Id
     */
    hCompId(hId: number): [number, number];
    tMeshId(comp: number, tId: number): number;
    tCompId(tId: number): [number, number];
    /**
     *
     * @param data Layer data
     * @param updateNormals Force normals computation
     */
    load(data: ILayerFeature[], updateNormals?: boolean): void;
    private setFunctionValues;
    private getFunctionValues;
    loadFunctionData(functionValues: number[][] | null | undefined, knotId: string): void;
    /**
     * Adds a new component to the mesh.
     * @param geometry triangulation of the feature
     */
    addComponent(geometry: IFeatureGeometry): void;
    buildOpposites(): void;
    buildVertexHe(): void;
    fixOrientation(): void;
    computeNormals(): void;
    getCoordinatesVBO(centroid: number[] | Float32Array | undefined, viewId: number): number[];
    getNormalsVBO(): number[];
    getFunctionVBO(knotId: string): number[][];
    getIndicesVBO(): number[];
    getIdsVBO(): number[];
    getHeightsVBO(): number[][];
    getMinHeightsVBO(): number[][];
    getOrientedEnvelopesVBO(centroid?: number[] | Float32Array): number[][][];
    getSectionFootprintVBO(centroid?: number[] | Float32Array): number[][][];
    getuvVBO(): number[];
    getWidthVBO(): number[];
    getHeightInSectionVBO(): number[];
    getSectionHeightVBO(): number[];
    getDiscardFuncIntervalVBO(): number[];
    /**
     * Returns the amount of cells in the mesh
     */
    idsLength(): number;
    /**
     * Returns the cells ids of all coordinates in the mesh. The cells ids are separated by component of the mesh. But in the context of each component each position stores the cell id of the corresponding coordinate as if the whole vector was flat.
     */
    getIdsCoordinates(): number[][];
    /**
     * Returns the number of coordinates per component of the mesh
     */
    getCoordsPerComp(): number[];
    /**
     * Returns the number of ids per component of the mesh
     */
    getNumIdsPerComp(): number[];
    /**
     *
     * @returns total number of coordinates considering all components
     */
    getTotalNumberOfCoords(): number;
    setFiltered(bbox: number[]): void;
    getAttachedKnots(): string[];
}

declare abstract class Shader {
    protected _shaderProgram: WebGLShader;
    protected _currentKnot: IKnot | IExKnot;
    protected _grammarInterpreter: any;
    /**
     * Default constructor
     * @param vsSource
     * @param fsSource
     * @param glContext
     */
    constructor(vsSource: string, fsSource: string, glContext: WebGL2RenderingContext, grammarInterpreter: any);
    get currentKnot(): IKnot | IExKnot;
    /**
     * Update the VBOs of the layer
     * @param {Mesh} mesh Updates the mesh data
     */
    abstract updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array, viewId: number): void;
    /**
     * Update the VBOs of the layer
     * @param {Mesh} mesh Updates the mesh data
     */
    abstract updateShaderData(mesh: Mesh, knot: IKnot | IExKnot): void;
    /**
    * Update the VBOs of the layer
    * @param {any} data Updates the layer data
    */
    abstract updateShaderUniforms(data: any): void;
    /**
     * Creates the uniforms name
     * @param {WebGL2RenderingContext} glContext WebGL context
     */
    abstract createUniforms(glContext: WebGL2RenderingContext): void;
    /**
     * Associates data to the uniforms
     * @param {WebGL2RenderingContext} glContext WebGL context
     * @param {Camera} camera The camera object
     */
    abstract bindUniforms(glContext: WebGL2RenderingContext, camera: any): void;
    /**
     * Creates the array of VBOs
     * @param {WebGL2RenderingContext} glContext WebGL context
     */
    abstract createTextures(glContext: WebGL2RenderingContext): void;
    /**
     * Associates data to the VBO
     * @param {WebGL2RenderingContext} glContext WebGL context
     * @param {Mesh} mesh The layer mesh
     */
    abstract bindTextures(glContext: WebGL2RenderingContext): void;
    /**
     * Creates the array of VBOs
     * @param {WebGL2RenderingContext} glContext WebGL context
     */
    abstract createVertexArrayObject(glContext: WebGL2RenderingContext): void;
    /**
     * Associates data to the VBO
     * @param {WebGL2RenderingContext} glContext WebGL context
     * @param {Mesh} mesh The layer mesh
     */
    abstract bindVertexArrayObject(glContext: WebGL2RenderingContext, mesh: Mesh): void;
    /**
     * Render pass
     * @param {WebGL2RenderingContext} glContext WebGL context
     * @param {Camera} camera The camera object
     * @param {Mesh} mesh The layer mesh
     */
    abstract renderPass(glContext: WebGL2RenderingContext, glPrimitive: number, camera: any, mesh: Mesh, zOrder: number): void;
    /**
     *
     * @param coordinates coordinates index to highlight
     */
    abstract setHighlightElements(coordinates: number[], value: boolean): void;
    abstract setFiltered(filtered: number[]): void;
    /**
    * Inits the layer's shader program
    * @param {string} vsSource Vertex shader source
    * @param {string} fsSource Fragment shader source
    * @param {WebGL2RenderingContext} glContext WebGL context
    */
    protected initShaderProgram(vsSource: string, fsSource: string, glContext: WebGL2RenderingContext): void;
    /**
     * Builds the layer shader
     * @param {number} type The shader type
     * @param {string} source The shader source string
     * @param {WebGL2RenderingContext} glContext The WebGL context
     * @returns {WebGLShader} The shader object
     */
    protected buildShader(type: number, source: string, glContext: WebGL2RenderingContext): WebGLShader | null;
    protected exportInteractions(colorOrPicked: number[], coordsPerComp: number[], knotId: string): void;
}

/**
 * Abstract class for the picking auxiliary shaders
 */

declare abstract class AuxiliaryShader extends Shader {
    /**
     * Receives picked cells ids
     * @param {Set<number>} pickedCells
     */
    abstract setPickedCells(pickedCells: Set<number>): void;
    /**
     * Set the id of the cell picked for the footprint vis
     * @param cellId Id of the cell picked for the footprint vis
     */
    abstract setPickedFoot(cellId: number, pickingForUpdate: boolean): void;
    /**
     * Set the id of the cell picked for the building highlighting
     * @param cellIds Ids of the cell picked
     */
    abstract setPickedObject(cellIds: number[]): void;
    /**
     * Receives the cell id by coordinate
     * @param {number[]} cellIdsByCoordinates
     */
    abstract setIdsCoordinates(cellIdsByCoordinates: number[][]): void;
    abstract clearPicking(): void;
}

declare abstract class Layer {
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

declare class BuildingsLayer extends Layer {
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

/**
 * 3D Camera representation
 */
declare class Camera {
    protected wOrigin: vec2;
    protected wEye: vec3;
    protected wEyeDir: vec3;
    protected wEyeLength: number;
    protected wLookAt: vec3;
    protected wUp: vec3;
    protected wNear: number;
    protected wFar: number;
    protected groundRes: number;
    protected fovy: number;
    protected mProjectionMatrix: mat4;
    protected mViewMatrix: mat4;
    protected mModelMatrix: mat4;
    protected _updateStatusCallback: any;
    private viewportWidth;
    private viewportHeight;
    constructor(initialPosition: number[], wUp: number[], wLookAt: number[], wEye: number[], updateStatusCallback: any);
    resetCamera(initialPosition: number[], wUp: number[], wLookAt: number[], wEye: number[], updateStatusCallback: any): void;
    getProjectionMatrix(): Float32Array | number[];
    getViewMatrix(): Float32Array | number[];
    getModelViewMatrix(): Float32Array | number[];
    getWorldOrigin(): Float32Array | number[];
    getEye(): Float32Array | number[];
    getGroundResolution(): number;
    setViewportResolution(x: number, y: number): void;
    getViewportResolution(): number[];
    updateEyeDirAndLen(): void;
    zScaling(scale: number): void;
    zoom(delta: number, x: number, y: number): void;
    translate(dx: number, dy: number): void;
    yaw(delta: number): void;
    pitch(delta: number): void;
    update(): void;
    getZoomLevel(): number;
    loadPosition(state: any): void;
    screenCoordToWorldDir(x: number, y: number): vec3;
    getUpVector(): vec3;
    getRightVector(): vec3;
    screenCoordToLatLng(x: number, y: number): number[] | null;
    setPosition(x: number, y: number): void;
    activateBirdsEye(): void;
}

declare abstract class ColorMap {
    protected static interpolator: (t: number) => string;
    static getColor(value: number, color: string): number[];
    static getColorMap(color: string, res?: number): number[];
}

declare class ServerlessApi {
    mapData: IMasterGrammar | IMapGrammar | IPlotGrammar | null;
    mapStyle: IMapStyle | null;
    carameraParameters: ICameraData | null;
    layers: ILayerData[] | null;
    layersFeature: ILayerFeature[] | null;
    joinedJsons: IJoinedJson[] | IExternalJoinedJson[] | null;
    components: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[] | null;
    interactionCallbacks: any;
    setComponents(components: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[]): Promise<void>;
    setLayers(layers: ILayerData[]): Promise<void>;
    setJoinedJsons(joinedJsons: IJoinedJson[] | IExternalJoinedJson[]): Promise<void>;
    addInteractionCallback: (knotId: string, callback: any) => void;
}

declare abstract class DataApi {
    /**
     * Load all layers
     * @param {string} index The layers index file
     */
    static getMapData(index: string, serverlessApi: ServerlessApi): Promise<IMasterGrammar | IMapGrammar | IPlotGrammar>;
    /**
     * @param {string} componentId The id of the component
     */
    static getComponentData(componentId: string, serverlessApi: ServerlessApi): Promise<IMapGrammar | IPlotGrammar>;
    /**
     * Load a custom style
     * @param {string} style The style file
     */
    static getCustomStyle(style: string, serverlessApi: ServerlessApi): Promise<IMapStyle>;
    /**
     * Load the camera
     * @param {string} camera The camera file
     */
    static getCameraParameters(camera: string, serverlessApi: ServerlessApi): Promise<ICameraData>;
    /**
     * Gets the layer data
     * @param {string} layerId the layer data
     */
    static getLayer(layerId: string, serverlessApi: ServerlessApi): Promise<ILayerData>;
    /**
     * Gets the layer data
     * @param {string} layerId the layer data
     */
    static getLayerFeature(layerId: string, serverlessApi: ServerlessApi): Promise<ILayerFeature[]>;
    static getJoinedJson(layerId: string, serverlessApi: ServerlessApi): Promise<IJoinedJson | IExternalJoinedJson>;
}

declare abstract class DataLoader {
    /**
     * Loads a json file
     * @param {string} url json file url
     * @returns {Promise<unknown>} The load json promise
     */
    static getJsonData(url: string): Promise<unknown>;
    static getBinaryData(url: string, type: string): Promise<unknown>;
    /**
     * Loads a text file
     * @param {string} url text file url
     * @returns {Promise<string>} The load text promise
     */
    static getTextData(url: string): Promise<string>;
}

declare class Environment {
    static backend: string;
    static serverless: boolean;
    /**
     * Set environment parameters
     * @param {{backend: string}} env Environment parameters
     */
    static setEnvironment(env: {
        backend: string;
    }): void;
}

declare abstract class GeoUtils {
    static res: number;
    static wLevel: number;
    /**
     * Converts from lat, lng to world coordinates
     * @param {number} latitude the latitude of the point
     * @param {number} longitude the longitude of the point
     */
    static latLng2Coord_old(latitude: number, longitude: number): number[];
    static latLng2Coord(latitude: number, longitude: number): number[];
    /**
     * Converts from world coordinates to lat, lng
     * @param {number} x the x coordinate of the point
     * @param {number} y the y coordinate of the point
     */
    static coord2LatLng_old(x: number, y: number): number[];
    static coord2LatLng(x: number, y: number): number[];
    /**
     * Computes the ground resolution
     * @param {number} lat the latitude value
     * @param {number} lng the longitude value
     * @param {number} zoom the zoom leevl
     */
    static groundResolution(lat: number, lng: number, zoom: number): number;
    static latlonToWebMercator(lat: number, lon: number): number[];
}

declare class KeyEvents {
    private _map;
    setMap(map: any): void;
    bindEvents(): void;
    /**
    * Handles key up event
    * @param {KeyboardEvent} event The fired event
    */
    keyUp(event: KeyboardEvent): Promise<void>;
}

declare class LayerManager {
    protected _layers: Layer[];
    protected _filterBbox: number[];
    protected _updateStatusCallback: any;
    protected _grammarInterpreter: any;
    constructor(grammarInterpreter: any);
    init(updateStatusCallback?: any | null): void;
    /**
     * Layers vector accessor
     * @returns {Layer[]} The array of layers
     */
    get layers(): Layer[];
    set filterBbox(bbox: number[]);
    /**
    * Creates a layer from the server
    * @param {string} layerType layer type
    * @param {string} layerId layer identifier
    * @returns {Layer | null} The load layer promise
    */
    createLayer(layerInfo: ILayerData, features: ILayerFeature[]): Layer | null;
    getJoinedObjects(layer: Layer, linkDescription: ILinkDescription): IJoinedObjects | null;
    getValuesExKnot(layerId: string, in_name: string): number[][];
    getAbstractDataFromLink(linkScheme: ILinkDescription[]): number[][] | null;
    searchByLayerInfo(layerInfo: ILayerData): Layer | null;
    searchByLayerId(layerId: string): Layer | null;
}

declare class LinesLayer extends Layer {
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

/**
 * Abstract class for the picking auxiliary shaders
 */

declare abstract class AuxiliaryShaderTriangles extends Shader {
    abstract setPickedObject(objectId: number[]): void;
    abstract clearPicking(): void;
}

declare class PointsLayer extends Layer {
    protected _coordsByCOORDINATES3D: number[][];
    protected _dimensions: number;
    protected _highlightByCOORDINATES: boolean[][];
    protected _highlightByCOORDINATES3D: boolean[][];
    protected _highlightByOBJECTS: boolean[][];
    constructor(info: ILayerData, zOrder: number | undefined, geometryData: ILayerFeature[]);
    supportInteraction(eventName: string): boolean;
    updateMeshGeometry(data: ILayerFeature[]): void;
    updateShaders(shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    getSelectedFiltering(): number[] | null;
    directAddMeshFunction(functionValues: number[][], knotId: string): void;
    updateFunction(knot: IKnot | IExKnot, shaders: (Shader | AuxiliaryShader)[]): void;
    render(glContext: WebGL2RenderingContext, shaders: (Shader | AuxiliaryShader)[]): void;
    setHighlightElements(elements: number[], level: LevelType, value: boolean, shaders: (Shader | AuxiliaryShader)[], centroid: number[] | Float32Array | undefined, viewId: number): void;
    highlightElement(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[]): void;
    getIdLastHighlightedElement(shaders: (Shader | AuxiliaryShaderTriangles)[]): number[] | undefined;
    highlightElementsInArea(glContext: WebGL2RenderingContext, x: number, y: number, shaders: (Shader | AuxiliaryShader)[], radius: number): void;
    distributeFunctionValues(functionValues: number[][] | null): number[][] | null;
    innerAggFunc(functionValues: number[] | null, startLevel: LevelType, endLevel: LevelType, operation: OperationType): number[] | null;
    getFunctionValueIndexOfId(id: number, level: LevelType): number | null;
    getCoordsByLevel(level: LevelType, centroid: number[] | Float32Array | undefined, viewId: number): number[][];
    getFunctionByLevel(level: LevelType, knotId: string): number[][][];
    getHighlightsByLevel(level: LevelType): boolean[];
}

declare class TrianglesLayer extends Layer {
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

declare class MapStyle {
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

declare class PlotManager {
    protected _plots: {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[];
    protected _filtered: any;
    protected _updateStatusCallback: any;
    protected _setGrammarUpdateCallback: any;
    protected _plotsKnotsData: {
        knotId: string;
        physicalId: string;
        allFilteredIn: boolean;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            filteredIn: boolean;
            index: number;
        }[];
    }[];
    protected _activeKnotPhysical: any;
    protected _setHighlightElementCallback: {
        function: any;
        arg: any;
    };
    protected _plotsReferences: any[];
    protected _needToUnHighlight: boolean;
    protected _highlightedVegaElements: any[];
    protected _id: string;
    /**
     * @param viewData
     * @param setGrammarUpdateCallback Function that sets the callback that will be called in the frontend to update the grammar
     */
    constructor(id: string, plots: {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[], plotsKnotsData: {
        knotId: string;
        physicalId: string;
        allFilteredIn: boolean;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            filteredIn: boolean;
            index: number;
        }[];
    }[], setHighlightElementCallback: {
        function: any;
        arg: any;
    });
    physicalKnotActiveChannel(message: {
        physicalId: string;
        knotId: string;
    }, _this: any): void;
    init(updateStatusCallback: any): void;
    updateGrammarPlotsData(plotsKnotsData: {
        knotId: string;
        physicalId: string;
        allFilteredIn: boolean;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            filteredIn: boolean;
            index: number;
        }[];
    }[]): Promise<void>;
    proccessKnotData(): any;
    clearFiltersLocally(knotsIds: string[]): void;
    clearHighlightsLocally(knotsIds: string[]): void;
    applyInteractionEffectsLocally(elements: any, truthValue: boolean, toggle?: boolean, fromMap?: boolean): void;
    clearInteractionEffectsLocally(knotsIds: string[]): void;
    setHighlightElementsLocally(elements: any, truthValue: boolean, toggle?: boolean): void;
    setFilterElementsLocally(elements: any, truthValue: boolean, toggle?: boolean): void;
    updatePlotsActivePhysical(): void;
    updatePlotsNewData(): void;
    attachPlots(processedKnotData: any): Promise<void>;
    getAbstractValues(functionIndex: number, knotsId: string[], plotsKnotsData: {
        knotId: string;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            index: number;
        }[];
    }[]): any;
    getHTMLFromVega(plot: any): Promise<HTMLImageElement>;
    getFootEmbeddedSvg(data: any, plotWidth: number, plotHeight: number): Promise<HTMLImageElement | null>;
    getSurEmbeddedSvg(data: any, plotWidth: number, plotHeight: number): Promise<HTMLImageElement | null>;
}

declare class Knot {
    protected _physicalLayer: Layer;
    protected _thematicData: number[][] | null;
    protected _knotSpecification: IKnot | IExKnot;
    protected _id: string;
    protected _shaders: any;
    protected _visible: boolean;
    protected _grammarInterpreter: any;
    protected _maps: any;
    protected _cmap: string;
    protected _range: number[];
    protected _domain: number[];
    protected _scale: string;
    constructor(id: string, physicalLayer: Layer, knotSpecification: IKnot | IExKnot, grammarInterpreter: any, visible: boolean);
    get id(): string;
    get visible(): boolean;
    get shaders(): any;
    get physicalLayer(): Layer;
    get knotSpecification(): IKnot | IExKnot;
    get thematicData(): number[][] | null;
    get cmap(): string;
    get range(): number[];
    get domain(): number[];
    get scale(): string;
    set visible(visible: boolean);
    set thematicData(thematicData: number[][] | null);
    addMap(map: any, viewId: number): void;
    render(glContext: WebGL2RenderingContext, camera: any, viewId: number): void;
    updateTimestep(timestep: number, viewId: number): void;
    overwriteSelectedElements(externalSelected: number[], viewId: number): void;
    loadShaders(glContext: WebGL2RenderingContext, centroid: number[] | Float32Array | undefined, viewId: number): void;
    addMeshFunction(layerManager: LayerManager): void;
    processThematicData(layerManager: LayerManager): void;
    private _getPickingArea;
    interact(glContext: WebGL2RenderingContext, eventName: string, mapGrammar: IMapGrammar, cursorPosition?: number[] | null, brushingPivot?: number[] | null, eventObject?: any | null): Promise<void>;
}

declare class KnotManager {
    protected _knots: Knot[];
    protected _updateStatusCallback: any;
    init(updateStatusCallback: any): void;
    get knots(): Knot[];
    createKnot(id: string, physicalLayer: Layer, knotSpecification: IKnot | IExKnot, grammarInterpreter: any, visible: boolean): Knot;
    toggleKnot(id: string, value?: boolean | null): void;
    overwriteSelectedElements(externalSelected: number[], layerId: string, viewId: number): void;
    getKnotById(knotId: string): Knot | null;
}

declare class MapView {
    protected _mapDiv: HTMLElement;
    protected _canvas: HTMLCanvasElement;
    _glContext: WebGL2RenderingContext;
    protected _layerManager: LayerManager;
    protected _knotManager: KnotManager;
    protected _plotManager: PlotManager;
    protected _grammarInterpreter: any;
    protected _updateStatusCallback: any;
    private _camera;
    private _mouse;
    private _keyboard;
    private _knotVisibilityMonitor;
    protected _embeddedKnots: Set<string>;
    protected _linkedKnots: Set<string>;
    _viewId: number;
    _mapGrammar: IMapGrammar;
    constructor(grammarInterpreter: any, layerManager: LayerManager, knotManager: KnotManager, viewId: number, mapGrammar: IMapGrammar);
    resetMap(grammarInterpreter: any, layerManager: LayerManager, knotManager: KnotManager, viewId: number, mapGrammar: IMapGrammar): void;
    get layerManager(): LayerManager;
    get mapGrammar(): IMapGrammar;
    get knotManager(): KnotManager;
    get mouse(): any;
    get viewId(): number;
    /**
     * gets the map div
     */
    get div(): HTMLElement;
    /**
     * gets the canvas element
     */
    get canvas(): HTMLCanvasElement;
    /**
     * gets the opengl context
     */
    get glContext(): WebGL2RenderingContext;
    /**
     * gets the camera object
     */
    get camera(): any;
    get plotManager(): PlotManager;
    updateTimestep(message: any, _this: any): void;
    /**
     * Map initialization function
     */
    init(mapDivId: string, updateStatusCallback: any): Promise<void>;
    updateGrammarPlotsData(): void;
    updateGrammarPlotsHighlight(layerId: string, level: LevelType | null, elements: number[] | null, clear?: boolean): void;
    initPlotManager(): void;
    setHighlightElement(knotId: string, elementIndex: number, value: boolean, _this: any): void;
    toggleKnot(id: string, value?: boolean | null): void;
    /**
     * Camera initialization function
     * @param {string | ICameraData} data Object containing the camera. If data is a string, then it loads data from disk.
     */
    initCamera(camera: ICameraData | string): Promise<void>;
    /**
     * Inits the mouse events
     */
    initMouseEvents(): void;
    /**
     * Inits the mouse events
     */
    initKeyboardEvents(): void;
    setCamera(camera: {
        position: number[];
        direction: {
            right: number[];
            lookAt: number[];
            up: number[];
        };
    }): void;
    /**
     * Renders the map
     */
    render(): void;
    private monitorKnotVisibility;
    /**
     * Resizes the html canvas
     */
    resize(): void;
}

declare class GrammarInterpreter {
    protected _grammar: IMasterGrammar;
    protected _preProcessedGrammar: IMasterGrammar;
    protected _components_grammar: {
        id: string;
        originalGrammar: (IMapGrammar | IPlotGrammar);
        grammar: (IMapGrammar | IPlotGrammar | undefined);
        position: (IComponentPosition | undefined);
    }[];
    protected _lastValidationTimestep: number;
    protected _components: {
        id: string;
        type: ComponentIdentifier;
        obj: any;
        position: IComponentPosition;
    }[];
    protected _maps_widgets: {
        type: WidgetType;
        obj: any;
        grammarDefinition: IGenericWidget | undefined;
    }[];
    protected _frontEndCallback: any;
    protected _layerManager: LayerManager;
    protected _knotManager: KnotManager;
    protected _plotManager: PlotManager;
    protected _mainDiv: HTMLElement;
    protected _url: string;
    protected _root: Root;
    protected _ajv: any;
    protected _ajv_map: any;
    protected _ajv_plots: any;
    protected _viewReactElem: any;
    protected _serverlessApi: ServerlessApi;
    protected _id: string;
    protected _cameraUpdateCallback: any;
    get id(): string;
    get layerManager(): LayerManager;
    get knotManager(): KnotManager;
    get mainDiv(): HTMLElement;
    get preprocessedGrammar(): IMasterGrammar;
    get plotManager(): PlotManager;
    get serverlessApi(): ServerlessApi;
    constructor(id: string, grammar: IMasterGrammar, mainDiv: HTMLElement, jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]);
    resetGrammarInterpreter(grammar: IMasterGrammar, mainDiv: HTMLElement, jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]): void;
    setServerlessApi(jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]): void;
    /**
     * inits the window events
     */
    initWindowEvents(): void;
    initViews(mainDiv: HTMLElement, grammar: IMasterGrammar, originalGrammar: IMasterGrammar, components_grammar: {
        id: string;
        originalGrammar: (IMapGrammar | IPlotGrammar);
        grammar: (IMapGrammar | IPlotGrammar | undefined);
    }[]): void;
    validateMasterGrammar(grammar: IMasterGrammar): boolean;
    validateComponentGrammar(grammar: IMapGrammar | IPlotGrammar): boolean;
    overwriteSelectedElements(externalSelected: number[], layerId: string): void;
    processGrammar(grammar: IMasterGrammar): Promise<void>;
    updateComponentGrammar(component_grammar: IMapGrammar | IPlotGrammar, componentInfo?: any): void;
    replaceVariablesAndInitViews(): Promise<void>;
    initKnots(): void;
    /**
     * Add layer geometry and function
     */
    addLayer(layerData: ILayerData, joined: boolean): Promise<void>;
    initLayers(): Promise<void>;
    init(updateStatus: any): Promise<void>;
    private createSpatialJoins;
    getCamera(mapId?: number): ICameraData;
    getPlots(mapId?: number | null): {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[];
    getKnots(knotId?: string | null): IKnot[];
    getPremadeKnots(knotId?: string | null): IExKnot[] | undefined;
    getMap(mapId?: number): IMapGrammar;
    getFilterKnots(mapId?: number): (number | IConditionBlock)[] | undefined;
    getProcessedGrammar(): IMasterGrammar;
    evaluateLayerVisibility(layerId: string, mapId: number): boolean;
    evaluateKnotVisibility(knot: Knot, mapId: number): boolean;
    getKnotById(knotId: string): IExKnot | IKnot | undefined;
    getKnotOutputLayer(knot: IKnot | IExKnot): string;
    getKnotLastLink(knot: IKnot): ILinkDescription;
    parsePlotsKnotData(viewId?: number | null): {
        knotId: string;
        physicalId: string;
        allFilteredIn: boolean;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            filteredIn: boolean;
            index: number;
        }[];
    }[];
    private renderViews;
}

declare class MouseEvents {
    private _map;
    private _status;
    private _lastPoint;
    private _brushing;
    private _brushingPivot;
    private _brushingFilter;
    private _brushingFilterPivot;
    private _currentPoint;
    get lastPoint(): number[];
    get currentPoint(): number[];
    setMap(map: any): void;
    /**
     * Mouse events binding function
     */
    bindEvents(): void;
    /**
     * Handles mouse right click event
     * @param {MouseEvent} event The fired event
     */
    contextMenu(event: MouseEvent): void;
    /**
     * Handles mouse down event
     * @param {MouseEvent} event The fired event
     */
    mouseDown(event: MouseEvent): void;
    /**
     * Handles mouse move event
     * @param {MouseEvent} event The fired event
     */
    mouseMove(event: MouseEvent): void;
    /**
     * Handles mouse up event
     */
    mouseUp(event: MouseEvent): void;
    /**
     * Handles mouse down event
     * @param {WheelEvent} event The fired event
     */
    mouseWheel(event: WheelEvent): Promise<void>;
}

declare class Pointset {
    constructor();
}

declare class Polyline {
    constructor();
}

declare class ShaderFlatColor extends Shader {
    protected _coords: number[];
    protected _indices: number[];
    protected _coordsPerComp: number[];
    protected _globalColor: number[];
    protected _glCoords: WebGLBuffer | null;
    protected _glIndices: WebGLBuffer | null;
    protected _coordsDirty: boolean;
    protected _coordsId: number;
    protected _uModelViewMatrix: WebGLUniformLocation | null;
    protected _uProjectionMatrix: WebGLUniformLocation | null;
    protected _uWorldOrigin: WebGLUniformLocation | null;
    protected _uGlobalColor: WebGLUniformLocation | null;
    protected _filtered: number[];
    constructor(glContext: WebGL2RenderingContext, color: number[], grammarInterpreter: any);
    updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array | undefined, viewId: number): void;
    updateShaderData(mesh: Mesh, knot: IKnot | IExKnot, currentTimestepFunction?: number): void;
    updateShaderUniforms(data: any): void;
    setHighlightElements(coordinates: number[], value: boolean): void;
    setFiltered(filtered: number[]): void;
    createUniforms(glContext: WebGL2RenderingContext): void;
    bindUniforms(glContext: WebGL2RenderingContext, camera: any): void;
    createTextures(glContext: WebGL2RenderingContext): void;
    bindTextures(glContext: WebGL2RenderingContext): void;
    createVertexArrayObject(glContext: WebGL2RenderingContext): void;
    bindVertexArrayObject(glContext: WebGL2RenderingContext, mesh: Mesh): void;
    renderPass(glContext: WebGL2RenderingContext, glPrimitive: number, camera: any, mesh: Mesh, zOrder: number): void;
}

declare class InteractionChannel {
    static getGrammar: Function;
    static modifyGrammar: Function;
    static modifyGrammarVisibility: Function;
    static passedVariables: {
        [key: string]: any;
    };
    static setModifyGrammarVisibility(modifyGrammar: Function): void;
    static getModifyGrammarVisibility(): Function;
    static addToPassedVariables(name: string, value: any): void;
    static getPassedVariable(name: string): any;
    static sendData(variable: {
        name: string;
        value: any;
    }): void;
}

export { BuildingsLayer, Camera, ColorHEX, ColorMap, ComponentIdentifier, DataApi, DataLoader, Environment, GeoUtils, GrammarInterpreter, GrammarType, ICameraData, ICategory, IComponent, IComponentPosition, IConditionBlock, IExKnot, IExternalJoinedJson, IFeatureGeometry, IGenericWidget, IGrid, IJoinedJson, IJoinedLayer, IJoinedObjects, IKnot, IKnotGroup, IKnotVisibility, ILayerData, ILayerFeature, ILinkDescription, IMapGrammar, IMapStyle, IMasterGrammar, IPlotArgs, IPlotGrammar, InteractionChannel, InteractionEffectType, InteractionType, KeyEvents, Layer, LayerManager, LayerType, LevelType, LinesLayer, MapStyle, MapView, MapViewStatu, Mesh, MeshComponent, MouseEvents, OperationType, PlotArrangementType, PlotInteractionType, PointsLayer, Pointset, Polyline, RenderStyle, Shader, ShaderFlatColor, SpatialRelationType, TrianglesLayer, ViewArrangementType, WidgetType };
