/**
 * Abstract class for the picking auxiliary shaders
 */
import { Shader } from "./shader";
export declare abstract class AuxiliaryShaderTriangles extends Shader {
    abstract setPickedObject(objectId: number[]): void;
    abstract clearPicking(): void;
}
