import './GrammarPanel.css';
import { IComponentPosition, IMapGrammar, IMasterGrammar, IPlotGrammar } from "../interfaces";
import { GrammarType } from "../constants";
type GrammarPanelProps = {
    obj: any;
    viewId: string;
    initialGrammar: IMasterGrammar;
    componentsGrammar: {
        id: string;
        originalGrammar: IMapGrammar | IPlotGrammar;
        grammar: IMapGrammar | IPlotGrammar | undefined;
        position: IComponentPosition | undefined;
    }[];
    camera: {
        position: number[];
        direction: {
            right: number[];
            lookAt: number[];
            up: number[];
        };
    };
    filterKnots: number[];
    inputId: string;
    setCamera: any;
    addNewMessage: any;
    applyGrammarButtonId: string;
    linkMapAndGrammarId: string;
    activeGrammar: string;
    activeGrammarType: GrammarType;
    editGrammar: any;
};
export declare const GrammarPanelContainer: ({ obj, viewId, initialGrammar, componentsGrammar, camera, filterKnots, inputId, setCamera, addNewMessage, applyGrammarButtonId, linkMapAndGrammarId, activeGrammar, activeGrammarType, editGrammar }: GrammarPanelProps) => JSX.Element;
export {};
