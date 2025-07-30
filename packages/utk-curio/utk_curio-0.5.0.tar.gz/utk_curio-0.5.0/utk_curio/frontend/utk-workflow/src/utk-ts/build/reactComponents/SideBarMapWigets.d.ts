import { WidgetType } from "../constants";
import { IGenericWidget } from "../interfaces";
type SideBarMapWidgetsProps = {
    x: number;
    y: number;
    mapWidth: number;
    mapHeight: number;
    listLayers: any;
    knotVisibility: any;
    inputBarId: string;
    genericPlots: any;
    togglePlots: any;
    mapWidgets: {
        type: WidgetType;
        obj: any;
        grammarDefinition: IGenericWidget | undefined;
    }[];
    componentId: string;
    editGrammar: any;
    broadcastMessage: any;
};
export declare var GrammarPanelVisibility: boolean;
export declare const SideBarMapWidgets: ({ x, y, mapWidth, mapHeight, listLayers, knotVisibility, inputBarId, genericPlots, togglePlots, mapWidgets, componentId, editGrammar, broadcastMessage }: SideBarMapWidgetsProps) => JSX.Element;
export {};
