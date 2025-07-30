/**
 * Layer types definition
 */
export declare enum LayerType {
    POINTS_LAYER = "POINTS_LAYER",
    LINES_2D_LAYER = "LINES_2D_LAYER",
    LINES_3D_LAYER = "LINES_3D_LAYER",
    TRIANGLES_2D_LAYER = "TRIANGLES_2D_LAYER",
    TRIANGLES_3D_LAYER = "TRIANGLES_3D_LAYER",
    BUILDINGS_LAYER = "BUILDINGS_LAYER",
    HEATMAP_LAYER = "HEATMAP_LAYER"
}
/**
 * Render styles definition
 */
export declare enum RenderStyle {
    FLAT_COLOR = "FLAT_COLOR",
    FLAT_COLOR_MAP = "FLAT_COLOR_MAP",
    FLAT_COLOR_POINTS = "FLAT_COLOR_POINTS",
    FLAT_COLOR_POINTS_MAP = "FLAT_COLOR_POINTS_MAP",
    SMOOTH_COLOR = "SMOOTH_COLOR",
    SMOOTH_COLOR_MAP = "SMOOTH_COLOR_MAP",
    SMOOTH_COLOR_MAP_TEX = "SMOOTH_COLOR_MAP_TEX",
    PICKING = "PICKING",
    ABSTRACT_SURFACES = "ABSTRACT_SURFACES",
    OUTLINE = "OUTLINE",
    COLOR_POINTS = "COLOR_POINTS"
}
/**
 * Supported aggregations for layer linking
 */
export declare enum OperationType {
    MAX = "MAX",
    MIN = "MIN",
    AVG = "AVG",
    SUM = "SUM",
    COUNT = "COUNT",
    NONE = "NONE",
    DISCARD = "DISCARD"
}
export declare enum ViewArrangementType {
    LINKED = "LINKED",
    EMBEDDED = "EMBEDDED"
}
export declare enum PlotArrangementType {
    SUR_EMBEDDED = "SUR_EMBEDDED",
    FOOT_EMBEDDED = "FOOT_EMBEDDED",
    LINKED = "LINKED"
}
export declare enum GrammarType {
    PLOT = "PLOT",
    MAP = "MAP",
    MASTER = "MASTER"
}
export declare enum SpatialRelationType {
    INTERSECTS = "INTERSECTS",
    CONTAINS = "CONTAINS",
    WITHIN = "WITHIN",
    TOUCHES = "TOUCHES",
    CROSSES = "CROSSES",
    OVERLAPS = "OVERLAPS",
    NEAREST = "NEAREST",
    DIRECT = "DIRECT",
    INNERAGG = "INNERAGG"
}
export declare enum LevelType {
    COORDINATES = "COORDINATES",
    OBJECTS = "OBJECTS",
    COORDINATES3D = "COORDINATES3D"
}
export declare enum InteractionType {
    BRUSHING = "BRUSHING",
    PICKING = "PICKING",
    AREA_PICKING = "AREA_PICKING",
    NONE = "NONE"
}
export declare enum PlotInteractionType {
    CLICK = "CLICK",
    HOVER = "HOVER",
    BRUSH = "BRUSH"
}
export declare enum InteractionEffectType {
    FILTER = "FILTER",
    HIGHLIGHT = "HIGHLIGHT"
}
export declare enum ComponentIdentifier {
    MAP = "MAP",
    GRAMMAR = "GRAMMAR",
    PLOT = "PLOT"
}
export declare enum WidgetType {
    TOGGLE_KNOT = "TOGGLE_KNOT",
    SEARCH = "SEARCH",
    HIDE_GRAMMAR = "HIDE_GRAMMAR"
}
/**
 * Mapview interaction status
 */
export declare class MapViewStatu {
    static IDLE: number;
    static DRAG: number;
    static DRAG_RIGHT: number;
}
/**
 * Color type definition
 */
export type ColorHEX = `#${string}`;
