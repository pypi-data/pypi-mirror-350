import { LayerManager } from './layer-manager';
import { ICameraData, IMapGrammar } from './interfaces';
import { LevelType } from './constants';
import { PlotManager } from "./plot-manager";
import { KnotManager } from './knot-manager';
export declare class MapView {
    protected _mapDiv: HTMLElement;
    protected _canvas: HTMLCanvasElement;
    _glContext: WebGL2RenderingContext;
    protected _layerManager: LayerManager;
    protected _knotManager: KnotManager;
    protected _plotManager: PlotManager;
    protected _grammarInterpreter: any;
    protected _updateStatusCallback: any;
    private _camera;
    private _mouse;
    private _keyboard;
    private _knotVisibilityMonitor;
    protected _embeddedKnots: Set<string>;
    protected _linkedKnots: Set<string>;
    _viewId: number;
    _mapGrammar: IMapGrammar;
    constructor(grammarInterpreter: any, layerManager: LayerManager, knotManager: KnotManager, viewId: number, mapGrammar: IMapGrammar);
    resetMap(grammarInterpreter: any, layerManager: LayerManager, knotManager: KnotManager, viewId: number, mapGrammar: IMapGrammar): void;
    get layerManager(): LayerManager;
    get mapGrammar(): IMapGrammar;
    get knotManager(): KnotManager;
    get mouse(): any;
    get viewId(): number;
    /**
     * gets the map div
     */
    get div(): HTMLElement;
    /**
     * gets the canvas element
     */
    get canvas(): HTMLCanvasElement;
    /**
     * gets the opengl context
     */
    get glContext(): WebGL2RenderingContext;
    /**
     * gets the camera object
     */
    get camera(): any;
    get plotManager(): PlotManager;
    updateTimestep(message: any, _this: any): void;
    /**
     * Map initialization function
     */
    init(mapDivId: string, updateStatusCallback: any): Promise<void>;
    updateGrammarPlotsData(): void;
    updateGrammarPlotsHighlight(layerId: string, level: LevelType | null, elements: number[] | null, clear?: boolean): void;
    initPlotManager(): void;
    setHighlightElement(knotId: string, elementIndex: number, value: boolean, _this: any): void;
    toggleKnot(id: string, value?: boolean | null): void;
    /**
     * Camera initialization function
     * @param {string | ICameraData} data Object containing the camera. If data is a string, then it loads data from disk.
     */
    initCamera(camera: ICameraData | string): Promise<void>;
    /**
     * Inits the mouse events
     */
    initMouseEvents(): void;
    /**
     * Inits the mouse events
     */
    initKeyboardEvents(): void;
    setCamera(camera: {
        position: number[];
        direction: {
            right: number[];
            lookAt: number[];
            up: number[];
        };
    }): void;
    /**
     * Renders the map
     */
    render(): void;
    private monitorKnotVisibility;
    /**
     * Resizes the html canvas
     */
    resize(): void;
}
