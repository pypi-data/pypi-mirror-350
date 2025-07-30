import './MapRenderer.css';
import { WidgetType } from "../constants";
import { IGenericWidget } from "../interfaces";
type MapRendererProps = {
    obj: any;
    viewId: string;
    mapWidgets: {
        type: WidgetType;
        obj: any;
        grammarDefinition: IGenericWidget | undefined;
    }[];
    x: number;
    y: number;
    width: number;
    height: number;
    listLayers: any;
    knotVisibility: any;
    genericPlots: any;
    togglePlots: any;
    inputBarId: string;
    componentId: string;
    editGrammar: any;
    broadcastMessage: any;
};
export declare const MapRendererContainer: ({ obj, viewId, mapWidgets, x, y, width, height, listLayers, knotVisibility, genericPlots, togglePlots, inputBarId, componentId, editGrammar, broadcastMessage }: MapRendererProps) => JSX.Element;
export {};
