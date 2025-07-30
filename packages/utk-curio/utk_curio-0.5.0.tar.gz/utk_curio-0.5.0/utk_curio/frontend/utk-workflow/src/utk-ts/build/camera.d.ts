import { vec2, vec3, mat4 } from 'gl-matrix';
/**
 * 3D Camera representation
 */
export declare class Camera {
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
