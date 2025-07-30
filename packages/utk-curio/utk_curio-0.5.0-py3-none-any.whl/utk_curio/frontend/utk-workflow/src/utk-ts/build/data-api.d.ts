import { ICameraData, ILayerFeature, ILayerData, IMapStyle, IMasterGrammar, IMapGrammar, IPlotGrammar, IJoinedJson, IExternalJoinedJson } from './interfaces';
import { ServerlessApi } from './serverless-api';
export declare abstract class DataApi {
    /**
     * Load all layers
     * @param {string} index The layers index file
     */
    static getMapData(index: string, serverlessApi: ServerlessApi): Promise<IMasterGrammar | IMapGrammar | IPlotGrammar>;
    /**
     * @param {string} componentId The id of the component
     */
    static getComponentData(componentId: string, serverlessApi: ServerlessApi): Promise<IMapGrammar | IPlotGrammar>;
    /**
     * Load a custom style
     * @param {string} style The style file
     */
    static getCustomStyle(style: string, serverlessApi: ServerlessApi): Promise<IMapStyle>;
    /**
     * Load the camera
     * @param {string} camera The camera file
     */
    static getCameraParameters(camera: string, serverlessApi: ServerlessApi): Promise<ICameraData>;
    /**
     * Gets the layer data
     * @param {string} layerId the layer data
     */
    static getLayer(layerId: string, serverlessApi: ServerlessApi): Promise<ILayerData>;
    /**
     * Gets the layer data
     * @param {string} layerId the layer data
     */
    static getLayerFeature(layerId: string, serverlessApi: ServerlessApi): Promise<ILayerFeature[]>;
    static getJoinedJson(layerId: string, serverlessApi: ServerlessApi): Promise<IJoinedJson | IExternalJoinedJson>;
}
