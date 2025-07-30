export declare class TextureComponent {
    protected _glContext: WebGL2RenderingContext;
    protected _texImage: WebGLTexture | null;
    protected _htmlImage: HTMLImageElement | null;
    constructor(glContext: WebGL2RenderingContext);
    get texImage(): WebGLTexture | null;
    get htmlImage(): HTMLImageElement | null;
    loadTextureFromHtml(img: any): void;
}
