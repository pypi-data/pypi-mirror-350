import { Shader } from "./shader";
import { Mesh } from "./mesh";
import { AuxiliaryShader } from "./auxiliaryShader";
import { IExKnot, IKnot } from "./interfaces";
/**
 * This shader should only be used with the buildings layer
 */
export declare class ShaderPicking extends Shader {
    protected _coords: number[];
    protected _indices: number[];
    protected _cellIds: number[];
    protected _glCoords: WebGLBuffer | null;
    protected _glIndices: WebGLBuffer | null;
    protected _glCellIds: WebGLBuffer | null;
    protected _coordsDirty: boolean;
    protected _cellIdsDirty: boolean;
    protected _resizeDirty: boolean;
    protected _clickDirty: boolean;
    protected _pickFilterDirty: boolean;
    protected _footDirty: boolean;
    protected _pickObjectDirty: boolean;
    protected _pickingForUpdate: boolean;
    protected _pickObjectAreaDirty: boolean;
    protected _coordsId: number;
    protected _cellIdsId: number;
    protected _uModelViewMatrix: WebGLUniformLocation | null;
    protected _uProjectionMatrix: WebGLUniformLocation | null;
    protected _uWorldOrigin: WebGLUniformLocation | null;
    protected _uColorMap: WebGLUniformLocation | null;
    protected _texPicking: WebGLTexture | null;
    protected _depthBuffer: WebGLRenderbuffer | null;
    protected _frameBuffer: WebGLFramebuffer | null;
    protected _pixelX: number;
    protected _pixelY: number;
    protected _pixelXFilter: number;
    protected _pixelYFilter: number;
    protected _pickingWidth: number;
    protected _pickingHeight: number;
    protected _pickingFilterWidth: number;
    protected _pickingFilterHeight: number;
    protected _selectedFiltered: number[];
    protected _cellIdsByCoordinates: number[][];
    protected _footPixelX: number;
    protected _footPixelY: number;
    protected _currentPickedFoot: number;
    protected _filtered: number[];
    protected _objectPixelX: number;
    protected _objectPixelY: number;
    protected _pickedCells: Set<number>;
    protected _currentPickedCells: Set<number>;
    protected _auxiliaryShader: AuxiliaryShader;
    protected _coordsPerComp: number[];
    protected _pickingRadius: number;
    /**
     *
     * @param {AuxiliaryShader} auxiliaryShader The shader responsible for receiving picking data
     */
    constructor(glContext: WebGL2RenderingContext, auxiliaryShader: AuxiliaryShader, grammarInterpreter: any);
    /**
     * Sets the resize dirty information
     */
    set resizeDirty(resizeDirty: boolean);
    get selectedFiltered(): number[];
    updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array | undefined, viewId: number): void;
    setFiltered(filtered: number[]): void;
    updatePickPosition(pixelX: number, pixelY: number, width: number, height: number): void;
    updatePickFilterPosition(pixelX: number, pixelY: number, width: number, height: number): void;
    /**
     *
     * @param pixelX
     * @param pixelY
     * @param update indicates if this picking is for creating a new plot or updating
     */
    updateFootPosition(pixelX: number, pixelY: number, update: boolean): void;
    applyBrushing(): void;
    isFilteredIn(objectId: number): boolean;
    pickPixel(glContext: WebGL2RenderingContext): void;
    getBboxFiltered(mesh: Mesh): number[];
    protected objectFromCell: (cellId: number) => number;
    pickPixelFilter(glContext: WebGL2RenderingContext): void;
    pickFoot(glContext: WebGL2RenderingContext): void;
    pickObject(glContext: WebGL2RenderingContext): void;
    pickObjectArea(glContext: WebGL2RenderingContext): void;
    updatePickObjectPosition(pixelX: number, pixelY: number): void;
    updatePickObjectArea(pixelX: number, pixelY: number, radius: number): void;
    clearPicking(): void;
    updateShaderData(mesh: Mesh, knot: IKnot | IExKnot, currentTimestepFunction?: number): void;
    updateShaderUniforms(data: any): void;
    setHighlightElements(coordinates: number[], value: boolean): void;
    createUniforms(glContext: WebGL2RenderingContext): void;
    bindUniforms(glContext: WebGL2RenderingContext, camera: any): void;
    setFramebufferAttachmentSizes(glContext: WebGL2RenderingContext, width: number, height: number): void;
    createTextures(glContext: WebGL2RenderingContext): void;
    bindTextures(glContext: WebGL2RenderingContext): void;
    createVertexArrayObject(glContext: WebGL2RenderingContext): void;
    bindVertexArrayObject(glContext: WebGL2RenderingContext, mesh: Mesh): void;
    renderPass(glContext: WebGL2RenderingContext, glPrimitive: number, camera: any, mesh: Mesh, zOrder: number): void;
}
