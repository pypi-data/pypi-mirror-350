import { ILayerData, IMapGrammar, IPlotGrammar, IJoinedJson, IExternalJoinedJson, IMasterGrammar, IMapStyle, ICameraData, ILayerFeature } from './interfaces';
export declare class ServerlessApi {
    mapData: IMasterGrammar | IMapGrammar | IPlotGrammar | null;
    mapStyle: IMapStyle | null;
    carameraParameters: ICameraData | null;
    layers: ILayerData[] | null;
    layersFeature: ILayerFeature[] | null;
    joinedJsons: IJoinedJson[] | IExternalJoinedJson[] | null;
    components: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[] | null;
    interactionCallbacks: any;
    setComponents(components: {
        id: string;
        json: IMapGrammar | IPlotGrammar;
    }[]): Promise<void>;
    setLayers(layers: ILayerData[]): Promise<void>;
    setJoinedJsons(joinedJsons: IJoinedJson[] | IExternalJoinedJson[]): Promise<void>;
    addInteractionCallback: (knotId: string, callback: any) => void;
}
