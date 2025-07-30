import { IFeatureGeometry, ILayerFeature } from "./interfaces";
/**
 * Half-Edge mesh component
 */
export declare class MeshComponent {
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
export declare class Mesh {
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
