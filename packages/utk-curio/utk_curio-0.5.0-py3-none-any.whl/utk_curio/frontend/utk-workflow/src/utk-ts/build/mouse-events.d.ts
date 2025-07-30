export declare class MouseEvents {
    private _map;
    private _status;
    private _lastPoint;
    private _brushing;
    private _brushingPivot;
    private _brushingFilter;
    private _brushingFilterPivot;
    private _currentPoint;
    get lastPoint(): number[];
    get currentPoint(): number[];
    setMap(map: any): void;
    /**
     * Mouse events binding function
     */
    bindEvents(): void;
    /**
     * Handles mouse right click event
     * @param {MouseEvent} event The fired event
     */
    contextMenu(event: MouseEvent): void;
    /**
     * Handles mouse down event
     * @param {MouseEvent} event The fired event
     */
    mouseDown(event: MouseEvent): void;
    /**
     * Handles mouse move event
     * @param {MouseEvent} event The fired event
     */
    mouseMove(event: MouseEvent): void;
    /**
     * Handles mouse up event
     */
    mouseUp(event: MouseEvent): void;
    /**
     * Handles mouse down event
     * @param {WheelEvent} event The fired event
     */
    mouseWheel(event: WheelEvent): Promise<void>;
}
