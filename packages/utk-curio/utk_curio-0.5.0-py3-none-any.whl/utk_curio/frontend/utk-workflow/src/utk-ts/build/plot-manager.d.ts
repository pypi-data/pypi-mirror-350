import { IComponentPosition, IPlotGrammar } from './interfaces';
export declare class PlotManager {
    protected _plots: {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[];
    protected _filtered: any;
    protected _updateStatusCallback: any;
    protected _setGrammarUpdateCallback: any;
    protected _plotsKnotsData: {
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
    protected _activeKnotPhysical: any;
    protected _setHighlightElementCallback: {
        function: any;
        arg: any;
    };
    protected _plotsReferences: any[];
    protected _needToUnHighlight: boolean;
    protected _highlightedVegaElements: any[];
    protected _id: string;
    /**
     * @param viewData
     * @param setGrammarUpdateCallback Function that sets the callback that will be called in the frontend to update the grammar
     */
    constructor(id: string, plots: {
        id: string;
        knotsByPhysical: any;
        originalGrammar: IPlotGrammar;
        grammar: IPlotGrammar;
        position: IComponentPosition | undefined;
        componentId: string;
    }[], plotsKnotsData: {
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
    }[], setHighlightElementCallback: {
        function: any;
        arg: any;
    });
    physicalKnotActiveChannel(message: {
        physicalId: string;
        knotId: string;
    }, _this: any): void;
    init(updateStatusCallback: any): void;
    updateGrammarPlotsData(plotsKnotsData: {
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
    }[]): Promise<void>;
    proccessKnotData(): any;
    clearFiltersLocally(knotsIds: string[]): void;
    clearHighlightsLocally(knotsIds: string[]): void;
    applyInteractionEffectsLocally(elements: any, truthValue: boolean, toggle?: boolean, fromMap?: boolean): void;
    clearInteractionEffectsLocally(knotsIds: string[]): void;
    setHighlightElementsLocally(elements: any, truthValue: boolean, toggle?: boolean): void;
    setFilterElementsLocally(elements: any, truthValue: boolean, toggle?: boolean): void;
    updatePlotsActivePhysical(): void;
    updatePlotsNewData(): void;
    attachPlots(processedKnotData: any): Promise<void>;
    getAbstractValues(functionIndex: number, knotsId: string[], plotsKnotsData: {
        knotId: string;
        elements: {
            coordinates: number[];
            abstract: number[];
            highlighted: boolean;
            index: number;
        }[];
    }[]): any;
    getHTMLFromVega(plot: any): Promise<HTMLImageElement>;
    getFootEmbeddedSvg(data: any, plotWidth: number, plotHeight: number): Promise<HTMLImageElement | null>;
    getSurEmbeddedSvg(data: any, plotWidth: number, plotHeight: number): Promise<HTMLImageElement | null>;
}
