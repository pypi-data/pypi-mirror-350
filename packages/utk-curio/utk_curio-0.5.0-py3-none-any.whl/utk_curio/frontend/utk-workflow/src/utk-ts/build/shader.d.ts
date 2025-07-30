import { Mesh } from "./mesh";
import { IExKnot, IKnot } from "./interfaces";
export declare abstract class Shader {
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
