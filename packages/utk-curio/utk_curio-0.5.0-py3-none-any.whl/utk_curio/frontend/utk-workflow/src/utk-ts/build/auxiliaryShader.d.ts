/**
 * Abstract class for the picking auxiliary shaders
 */
import { Shader } from "./shader";
export declare abstract class AuxiliaryShader extends Shader {
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
