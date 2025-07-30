import { Mesh } from "./mesh";
import { AuxiliaryShader } from "./auxiliaryShader";
import { IExKnot, IKnot } from "./interfaces";
/**
 * This shader should only be used with the buildings layer
 */
export declare class ShaderSmoothColorMapTex extends AuxiliaryShader {
    protected _coords: number[];
    protected _normals: number[];
    protected _function: number[][];
    protected _currentTimestepFunction: number;
    protected _unchangedFunction: number[][];
    protected _indices: number[];
    protected _idsLength: number;
    protected _heights: number[][];
    protected _minHeights: number[][];
    protected _orientedEnvelope: number[][][];
    protected _sectionFootprint: number[][][];
    protected _footprintPlaneHeightByCoord: number[];
    protected _coordsPerComp: number[];
    protected _lastCode: number;
    protected _functionToUse: number;
    private _colorMap;
    private _colorMapReverse;
    private _range;
    private _domain;
    private _providedDomain;
    private _scale;
    protected _glCoords: WebGLBuffer | null;
    protected _glNormals: WebGLBuffer | null;
    protected _glFunction: WebGLBuffer | null;
    protected _glIndices: WebGLBuffer | null;
    protected _glColorOrPicked: WebGLBuffer | null;
    protected _glFootprintPlaneHeight: WebGLBuffer | null;
    protected _glFiltered: WebGLBuffer | null;
    protected _coordsDirty: boolean;
    protected _functionDirty: boolean;
    protected _colorMapDirty: boolean;
    protected _colorOrPickedDirty: boolean;
    protected _planeHeightDirty: boolean;
    protected _filteredDirty: boolean;
    protected _coordsId: number;
    protected _normalsId: number;
    protected _functionId: number;
    protected _colorOrPickedId: number;
    protected _planeHeightId: number;
    protected _filteredId: number;
    protected _uModelViewMatrix: WebGLUniformLocation | null;
    protected _uProjectionMatrix: WebGLUniformLocation | null;
    protected _uWorldOrigin: WebGLUniformLocation | null;
    protected _uColorMap: WebGLUniformLocation | null;
    protected _textureLocation: WebGLUniformLocation | null;
    protected _texColorMap: WebGLTexture | null;
    protected _colorOrPicked: number[];
    protected _cellIdsByCoordinates: number[][];
    protected _pickedCoordinates: number[];
    protected _footprintCoords: number[];
    protected _currentBuildingCoords: number[];
    protected _coordinatesById: number[][];
    protected _currentFootprintBuildingId: number;
    protected _currentPickedBuildingId: number[];
    protected _footprintCodesPerBuilding: {
        buildingId: number;
        code: number;
        plotHeight: number;
        plotType: number;
    }[];
    protected _auxCoords: number[];
    protected _auxIndices: number[];
    protected _auxNormals: number[];
    protected _auxFunction: number[];
    protected _filtered: number[];
    constructor(glContext: WebGL2RenderingContext, grammarInterpreter: any, colorMap?: string, range?: number[], domain?: number[], scale?: string, colorMapReverse?: boolean);
    get colorOrPicked(): number[];
    get currentFootPrintBuildingId(): number;
    get currentPickedBuildingId(): number[];
    updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array | undefined, viewId: number): void;
    setFiltered(filtered: number[]): void;
    normalizeFunction(mesh: Mesh, knot: IKnot | IExKnot): void;
    updateShaderData(mesh: Mesh, knot: IKnot | IExKnot, currentTimestepFunction?: number): void;
    updateShaderUniforms(data: any): void;
    createUniforms(glContext: WebGL2RenderingContext): void;
    bindUniforms(glContext: WebGL2RenderingContext, camera: any): void;
    createTextures(glContext: WebGL2RenderingContext): void;
    bindTextures(glContext: WebGL2RenderingContext): void;
    createVertexArrayObject(glContext: WebGL2RenderingContext): void;
    bindVertexArrayObject(glContext: WebGL2RenderingContext, mesh: Mesh): void;
    setIdsCoordinates(cellIdsByCoordinates: number[][]): void;
    setPickedCells(pickedCells: Set<number>): void;
    /**
     * Return all the coordinates indices of a specific building given that the this._coords array is grouped by building
     * @param buildingId id of the building in the coords array
     */
    getBuildingCoords(buildingId: number): number[];
    /**
     * Calculates footprint coords based on the building coords
     * @param buildingCoords
     */
    calcFootprintCoords(buildingCoords: number[]): void;
    /**
     * Calculates the surface mesh for the footprint plot.
     * It uses Principal Component Analysis to create a oriented bounding plane
     *
     * @param {number} deltaHeight how much to shift the height if it is updating a surface
     * @param {boolean} update if a footprint plot is being updated
     * @param {number} plotType the type of d3 plot to show (-1 in case of update to maintain the plot type)
     * @param {string} specType d3 for d3 plots and vega for vega-lite plots
     */
    applyFootprintPlot(spec: any, update: boolean, plotType?: number, deltaHeight?: number, specType?: string): Promise<{
        indices: never[];
        coords: never[];
        functionValues: never[];
        image: undefined;
        code?: undefined;
    } | {
        indices: number[];
        coords: number[];
        functionValues: number[];
        image: any;
        code: number;
    } | undefined>;
    setPickedFoot(cellId: number, pickingForUpdate: boolean): void;
    setPickedObject(cellIds: number[]): void;
    clearPicking(): void;
    setHighlightElements(coordinates: number[], value: boolean): void;
    /**
     * Determines the center and radius of smallest sphere that contains the picked coordinates
     */
    bSpherePickedCoords(): {
        center: number[];
        radius: number;
    };
    /**
     * Handles the generation of a custom texture defined by the user.
     */
    generateCustomTexture(spec: any, specType: string, data: string, width: number, height: number): Promise<any>;
    /**
     * Handles the generation of a custom texture defined by the user.
     */
    generateCustomTextureFoot(spec: any, data: string, width: number, height: number, conversionFactor: number, plotNumber: number, specType: string): Promise<any>;
    /**
     * Defines transformations necessary to make a surface flat having a z = 0 and to undo it
     *
     * @param {boolean} centerPlane center point of the plane
     * @param {boolean} normal the normal of the plane
     *
     */
    absSurfaceTrans(centerPlane: number[], normal: number[]): {
        do: number[][];
        undo: number[][];
    };
    /**
     * Get a flat list of numbers and converts to a column matrix
     * @param {number[]} flatArray flat list of nummbers
     * @param {number} dim number of rows in the matrix
     */
    private flatArrayToMatrix;
    applyTexSelectedCells(camera: any, spec: any, specType: string): Promise<{
        indices: number[];
        coords: number[];
        functionValues: number[];
        image: any;
        code: number;
    } | undefined>;
    overwriteSelectedElements(externalSelected: number[]): void;
    /**
     * Reset the data structures that keep track of instantiated surfaces
     */
    clearSurfaces(): void;
    /**
     * Calculate the sum of normals of the picked coordinates
     */
    sumPickedNormals(): number[];
    renderPass(glContext: WebGL2RenderingContext, glPrimitive: number, camera: any, mesh: Mesh, zOrder: number): void;
}
