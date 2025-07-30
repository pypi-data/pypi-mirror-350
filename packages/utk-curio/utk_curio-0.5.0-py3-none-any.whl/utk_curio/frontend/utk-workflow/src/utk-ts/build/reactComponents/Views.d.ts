import { ComponentIdentifier, WidgetType } from '../constants';
import './Dragbox.css';
import { IComponentPosition, IGenericWidget, IMapGrammar, IMasterGrammar, IPlotGrammar } from '../interfaces';
import './View.css';
type ViewProps = {
    viewObjs: {
        id: string;
        type: ComponentIdentifier;
        obj: any;
        position: IComponentPosition;
    }[];
    mapsWidgets: {
        type: WidgetType;
        obj: any;
        grammarDefinition: IGenericWidget | undefined;
    }[];
    viewIds: string[];
    grammar: IMasterGrammar;
    componentsGrammar: {
        id: string;
        originalGrammar: IMapGrammar | IPlotGrammar;
        grammar: IMapGrammar | IPlotGrammar | undefined;
        position: IComponentPosition | undefined;
    }[];
    mainDiv: any;
    grammarInterpreter: any;
};
declare function Views({ viewObjs, mapsWidgets, viewIds, grammar, componentsGrammar, mainDiv, grammarInterpreter }: ViewProps): JSX.Element;
export default Views;
