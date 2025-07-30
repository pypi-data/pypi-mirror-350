import { LayerType, RenderStyle, ColorHEX, OperationType, GrammarType, SpatialRelationType, LevelType, InteractionType, WidgetType, InteractionEffectType } from "./constants";
/**
 * Interface for master grammar
 */
export interface IMasterGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    components: (IComponent)[];
    knots: IKnot[];
    ex_knots?: IExKnot[];
    grid: IGrid;
    grammar: boolean;
    grammar_position?: IComponentPosition;
}
export interface IExKnot {
    id: string;
    out_name: string;
    in_name?: string;
    group?: IKnotGroup;
    color_map?: string | IConditionBlock;
    range?: number[];
    domain?: number[];
    scale?: string;
}
/**
 * Interface for map grammar
 */
export interface IMapGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    camera: ICameraData;
    knots: (string | IConditionBlock)[];
    interactions: (InteractionType | IConditionBlock)[];
    plot: {
        id: string;
    };
    filterKnots?: (number | IConditionBlock)[];
    knotVisibility?: IKnotVisibility[];
    widgets?: IGenericWidget[];
    grammar_type: GrammarType;
}
export interface IExternalJoinedJson {
    id: string;
    incomingId: string[];
    inValues: number[][][];
}
/**
 * Interface for plot grammar
 */
export interface IPlotGrammar {
    variables?: {
        name: string;
        value: string;
    }[];
    name: string;
    plot: any;
    arrangement: string;
    knots: string[];
    interaction: string;
    args?: IPlotArgs;
    interaction_effect?: InteractionEffectType;
    grammar_type: GrammarType;
}
export interface IComponent {
    id: string;
    position: IComponentPosition;
}
export interface IGrid {
    width: number;
    height: number;
}
export interface IGenericWidget {
    type: WidgetType;
    args?: {
        categories: ICategory[];
    };
}
export interface ICategory {
    category_name: string;
    elements: (string | ICategory)[];
}
export interface IComponentPosition {
    width: number[];
    height: number[];
}
export interface IPlotArgs {
    bins?: number | IConditionBlock;
}
export interface IKnot {
    id: string;
    group?: IKnotGroup;
    knot_op?: boolean;
    color_map?: string | IConditionBlock;
    integration_scheme: ILinkDescription[];
    range?: number[];
    domain?: number[];
    scale?: string;
}
export interface IKnotGroup {
    group_name: string;
    position: number;
}
export interface ILinkDescription {
    spatial_relation?: SpatialRelationType;
    out: {
        name: string;
        level: LevelType;
    };
    in?: {
        name: string;
        level: LevelType;
    };
    operation: OperationType | IConditionBlock;
    abstract?: boolean;
    op?: string;
    maxDistance?: number;
    defaultValue?: number;
}
/**
 * Interface with the camera definition
 */
export interface ICameraData {
    position: number[];
    direction: {
        right: number[];
        lookAt: number[];
        up: number[];
    };
}
/**
 * Interface with the layer style definition
 */
export interface IMapStyle {
    land: ColorHEX;
    roads: ColorHEX;
    parks: ColorHEX;
    water: ColorHEX;
    sky: ColorHEX;
    surface: ColorHEX;
    building: ColorHEX;
}
/**
 * Interface with the layer definition (Feature collection)
 */
export interface ILayerData {
    id: string;
    type: LayerType;
    styleKey: keyof IMapStyle;
    data?: ILayerFeature[];
    renderStyle?: RenderStyle[];
}
export interface IJoinedJson {
    joinedLayers: IJoinedLayer[];
    joinedObjects: IJoinedObjects[];
}
export interface IJoinedObjects {
    joinedLayerIndex: number;
    inValues?: number[] | number[][];
    inIds?: number[][];
}
export interface IJoinedLayer {
    spatial_relation: string;
    layerId: string;
    outLevel: string;
    inLevel: string;
    abstract: boolean;
}
/**
 * Interface with the Layer Feature definition (Feature: Geometry collection)
 */
export interface ILayerFeature {
    geometry: IFeatureGeometry;
    highlight?: boolean;
    highlightIds?: number[];
}
/**
 * Interface with the feature geometry definition (Geometry: Geometric info)
 */
export interface IFeatureGeometry {
    coordinates: number[];
    normals?: number[];
    function?: number[][];
    indices?: number[];
    ids?: number[];
    heights?: number[];
    minHeights?: number[];
    orientedEnvelope?: number[][];
    sectionFootprint?: number[][];
    uv?: number[];
    width?: number[];
    pointsPerSection?: number[];
    discardFuncInterval?: number[];
    varyOpByFunc?: number;
}
export interface IConditionBlock {
    condition: IConditionElement[];
}
interface IConditionElement {
    test?: string;
    value: any;
}
export interface IKnotVisibility {
    knot: string;
    test: string;
}
export {};
