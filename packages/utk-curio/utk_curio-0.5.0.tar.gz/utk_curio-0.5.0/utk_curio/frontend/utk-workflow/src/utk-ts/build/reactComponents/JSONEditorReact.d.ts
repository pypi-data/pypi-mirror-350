import { JSONEditorMode } from "jsoneditor";
import '../../node_modules/jsoneditor/dist/jsoneditor.min.css';
type GrammarEditorProps = {
    content: any;
    schema: any;
    schemaRefs: any;
    mode: JSONEditorMode;
    modes: string[];
    onChangeText: any;
    onModeChange: any;
    allowSchemaSuggestions: boolean;
    indentation: number;
};
export default function GrammarEditor({ content, schema, schemaRefs, mode, modes, onChangeText, onModeChange, allowSchemaSuggestions, indentation }: GrammarEditorProps): JSX.Element;
export {};
