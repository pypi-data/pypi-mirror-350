import { Shader } from "./shader";
import { Mesh } from "./mesh";
import { TextureComponent } from "./texture";
import { IExKnot, IKnot } from "./interfaces";
/**
 * This shader should only be used with the buildings layer
 */
export declare class ShaderAbstractSurface extends Shader {
    protected _glCoords: WebGLBuffer | null;
    protected _glFunction: WebGLBuffer | null;
    protected _glIndices: WebGLBuffer | null;
    protected _coordsDirty: boolean;
    protected _functionDirty: boolean;
    protected _coordsId: number;
    protected _functionId: number;
    protected _uModelViewMatrix: WebGLUniformLocation | null;
    protected _uProjectionMatrix: WebGLUniformLocation | null;
    protected _uWorldOrigin: WebGLUniformLocation | null;
    protected _textureLocation: WebGLUniformLocation | null;
    protected _absSurfaces: {
        indices: number[];
        coords: number[];
        functionValues: number[];
        texComponent: TextureComponent;
        code: number;
    }[];
    protected _currentIndexTexture: number;
    protected _footprintSurfaces: {
        indices: number[];
        coords: number[];
        functionValues: number[];
        texComponent: TextureComponent;
        code: number;
    }[];
    protected _currentSurfaceType: string;
    protected _filtered: number[];
    constructor(glContext: WebGL2RenderingContext, grammarInterpreter: any);
    /**
     * Get a HTMLImageElement[] containing all the images used in the abstract surfaces
     */
    getAbsSurfacesImages(): HTMLImageElement[];
    setHighlightElements(coordinates: number[], value: boolean): void;
    updateShaderGeometry(mesh: Mesh, centroid: number[] | Float32Array | undefined, viewId: number): void;
    updateShaderData(mesh: Mesh, knot: IKnot | IExKnot, currentTimestepFunction?: number): void;
    updateShaderUniforms(data: any): void;
    createTextures(): void;
    setFiltered(filtered: number[]): void;
    createUniforms(glContext: WebGL2RenderingContext): void;
    bindUniforms(glContext: WebGL2RenderingContext, camera: any): void;
    bindTextures(glContext: WebGL2RenderingContext): void;
    createVertexArrayObject(glContext: WebGL2RenderingContext): void;
    bindVertexArrayObject(glContext: WebGL2RenderingContext, mesh: Mesh): void;
    /**
     *
     * @param glContext WebGL context
     * @param image HTMLImageElement for the surface texture
     * @param coords coordinates of the four corners of the surface
     * @param indices indices of the triangles of the surface
     * @param functionValues texture coordinates
     * @param type "abs" for abstract surfaces, "foot" for footprint plot
     * @param code a unique code that identify the surface
     */
    addSurface(glContext: WebGL2RenderingContext, image: HTMLImageElement, coords: number[], indices: number[], functionValues: number[], type: string | undefined, code: number): void;
    /**
     * Updates the a specific surface previouly created
     *
     * @param glContext WebGL context
     * @param image HTMLImageElement for the surface texture
     * @param coords coordinates of the four corners of the surface
     * @param indices indices of the triangles of the surface
     * @param functionValues texture coordinates
     * @param type "abs" for abstract surfaces, "foot" for footprint plot
     * @param code a unique code that identify the surface
     */
    updateSurface(glContext: WebGL2RenderingContext, image: HTMLImageElement, coords: number[], indices: number[], functionValues: number[], type: string | undefined, code: number): void;
    clearSurfaces(): void;
    clearFootprintPlots(): void;
    clearAbsSurfaces(): void;
    renderPass(glContext: WebGL2RenderingContext, glPrimitive: number, camera: any, mesh: Mesh, zOrder: number): void;
}
