import { Layer } from './layer';
import { ILayerData, ILinkDescription, IJoinedObjects, ILayerFeature } from './interfaces';
export declare class LayerManager {
    protected _layers: Layer[];
    protected _filterBbox: number[];
    protected _updateStatusCallback: any;
    protected _grammarInterpreter: any;
    constructor(grammarInterpreter: any);
    init(updateStatusCallback?: any | null): void;
    /**
     * Layers vector accessor
     * @returns {Layer[]} The array of layers
     */
    get layers(): Layer[];
    set filterBbox(bbox: number[]);
    /**
    * Creates a layer from the server
    * @param {string} layerType layer type
    * @param {string} layerId layer identifier
    * @returns {Layer | null} The load layer promise
    */
    createLayer(layerInfo: ILayerData, features: ILayerFeature[]): Layer | null;
    getJoinedObjects(layer: Layer, linkDescription: ILinkDescription): IJoinedObjects | null;
    getValuesExKnot(layerId: string, in_name: string): number[][];
    getAbstractDataFromLink(linkScheme: ILinkDescription[]): number[][] | null;
    searchByLayerInfo(layerInfo: ILayerData): Layer | null;
    searchByLayerId(layerId: string): Layer | null;
}
