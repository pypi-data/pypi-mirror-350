import { Shader } from "./shader";
import { Mesh } from "./mesh";
import { AuxiliaryShaderTriangles } from "./auxiliaryShaderTriangles";
import { IExKnot, IKnot } from "./interfaces";
export declare class ShaderPickingTriangles extends Shader {
    protected _coords: number[];
    protected _indices: number[];
    protected _objectsIds: number[];
    protected _glCoords: WebGLBuffer | null;
    protected _glIndices: WebGLBuffer | null;
    protected _glObjectsIds: WebGLBuffer | null;
    protected _coordsDirty: boolean;
    protected _resizeDirty: boolean;
    protected _pickObjectDirty: boolean;
    protected _pickObjectAreaDirty: boolean;
    protected _objectsIdsDirty: boolean;
    protected _pickFilterDirty: boolean;
    protected _coordsId: number;
    protected _objectsIdsId: number;
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
    protected _filtered: number[];
    protected _objectPixelX: number;
    protected _objectPixelY: number;
    protected _auxiliaryShader: AuxiliaryShaderTriangles;
    protected _coordsPerComp: number[];
    protected _pickingRadius: number;
    /**
     *
     * @param {AuxiliaryShaderTriangles} auxiliaryShaderTriangles The shader responsible for receiving picking data
     */
    constructor(glContext: WebGL2RenderingContext, auxiliaryShaderTriangles: AuxiliaryShaderTriangles, grammarInterpreter: any);
    /**
     * Sets the resize dirty information
     */
    set resizeDirty(resizeDirty: boolean);
    get selectedFiltered(): number[];
    getBboxFiltered(mesh: Mesh): number[];
    updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array | undefined, viewId: number): void;
    setFiltered(filtered: number[]): void;
    updatePickPosition(pixelX: number, pixelY: number, width: number, height: number): void;
    updatePickFilterPosition(pixelX: number, pixelY: number, width: number, height: number): void;
    pickPixelFilter(glContext: WebGL2RenderingContext): void;
    isFilteredIn(objectId: number): boolean;
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
