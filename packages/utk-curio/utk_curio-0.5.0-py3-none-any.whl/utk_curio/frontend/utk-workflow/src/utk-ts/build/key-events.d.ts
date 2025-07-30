export declare class KeyEvents {
    private _map;
    setMap(map: any): void;
    bindEvents(): void;
    /**
    * Handles key up event
    * @param {KeyboardEvent} event The fired event
    */
    keyUp(event: KeyboardEvent): Promise<void>;
}
