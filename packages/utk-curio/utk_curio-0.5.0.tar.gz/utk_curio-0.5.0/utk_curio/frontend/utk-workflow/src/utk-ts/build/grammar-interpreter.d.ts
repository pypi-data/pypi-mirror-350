import { ICameraData, IConditionBlock, IMasterGrammar, IKnot, IMapGrammar, IPlotGrammar, IComponentPosition, IGenericWidget, ILayerData, IExKnot, ILinkDescription, IExternalJoinedJson } from './interfaces';
import { ComponentIdentifier, WidgetType } from './constants';
import { Knot } from './knot';
import { Root } from 'react-dom/client';
import { LayerManager } from './layer-manager';
import { KnotManager } from './knot-manager';
import { PlotManager } from './plot-manager';
import { ServerlessApi } from './serverless-api';
export declare class GrammarInterpreter {
    protected _grammar: IMasterGrammar;
    protected _preProcessedGrammar: IMasterGrammar;
    protected _components_grammar: {
        id: string;
        originalGrammar: (IMapGrammar | IPlotGrammar);
        grammar: (IMapGrammar | IPlotGrammar | undefined);
        position: (IComponentPosition | undefined);
    }[];
    protected _lastValidationTimestep: number;
    protected _components: {
        id: string;
        type: ComponentIdentifier;
        obj: any;
        position: IComponentPosition;
    }[];
    protected _maps_widgets: {
        type: WidgetType;
        obj: any;
        grammarDefinition: IGenericWidget | undefined;
    }[];
    protected _frontEndCallback: any;
    protected _layerManager: LayerManager;
    protected _knotManager: KnotManager;
    protected _plotManager: PlotManager;
    protected _mainDiv: HTMLElement;
    protected _url: string;
    protected _root: Root;
    protected _ajv: any;
    protected _ajv_map: any;
    protected _ajv_plots: any;
    protected _viewReactElem: any;
    protected _serverlessApi: ServerlessApi;
    protected _id: string;
    protected _cameraUpdateCallback: any;
    get id(): string;
    get layerManager(): LayerManager;
    get knotManager(): KnotManager;
    get mainDiv(): HTMLElement;
    get preprocessedGrammar(): IMasterGrammar;
    get plotManager(): PlotManager;
    get serverlessApi(): ServerlessApi;
    constructor(id: string, grammar: IMasterGrammar, mainDiv: HTMLElement, jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]);
    resetGrammarInterpreter(grammar: IMasterGrammar, mainDiv: HTMLElement, jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]): void;
    setServerlessApi(jsonLayers?: ILayerData[], joinedJsons?: IExternalJoinedJson[], components?: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[], interactionCallbacks?: {
        knotId: string;
        callback: any;
    }[]): void;
    /**
     * inits the window events
     */
    initWindowEvents(): void;
    initViews(mainDiv: HTMLElement, grammar: IMasterGrammar, originalGrammar: IMasterGrammar, components_grammar: {
        id: string;
        originalGrammar: (IMapGrammar | IPlotGrammar);
        grammar: (IMapGrammar | IPlotGrammar | undefined);
    }[]): void;
    validateMasterGrammar(grammar: IMasterGrammar): boolean;
    validateComponentGrammar(grammar: IMapGrammar | IPlotGrammar): boolean;
    overwriteSelectedElements(externalSelected: number[], layerId: string): void;
    processGrammar(grammar: IMasterGrammar): Promise<void>;
    updateComponentGrammar(component_grammar: IMapGrammar | IPlotGrammar, componentInfo?: any): void;
    replaceVariablesAndInitViews(): Promise<void>;
    initKnots(): void;
    /**
     * Add layer geometry and function
     */
    addLayer(layerData: ILayerData, joined: boolean): Promise<void>;
    initLayers(): Promise<void>;
    init(updateStatus: any): Promise<void>;
    private createSpatialJoins;
    getCamera(mapId?: number): ICameraData;
    getPlots(mapId?: number | null): {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[];
    getKnots(knotId?: string | null): IKnot[];
    getPremadeKnots(knotId?: string | null): IExKnot[] | undefined;
    getMap(mapId?: number): IMapGrammar;
    getFilterKnots(mapId?: number): (number | IConditionBlock)[] | undefined;
    getProcessedGrammar(): IMasterGrammar;
    evaluateLayerVisibility(layerId: string, mapId: number): boolean;
    evaluateKnotVisibility(knot: Knot, mapId: number): boolean;
    getKnotById(knotId: string): IExKnot | IKnot | undefined;
    getKnotOutputLayer(knot: IKnot | IExKnot): string;
    getKnotLastLink(knot: IKnot): ILinkDescription;
    parsePlotsKnotData(viewId?: number | null): {
        knotId: string;
        physicalId: string;
        allFilteredIn: boolean;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            filteredIn: boolean;
            index: number;
        }[];
    }[];
    private renderViews;
}
