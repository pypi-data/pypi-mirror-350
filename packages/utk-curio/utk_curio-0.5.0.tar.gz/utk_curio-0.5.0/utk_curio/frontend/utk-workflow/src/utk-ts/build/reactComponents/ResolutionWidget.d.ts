import './ResolutionWidget.css';
type ResolutionWidgetProps = {
    obj: any;
    listLayers: string[];
    viewId: string;
    camera: {
        position: number[];
        direction: {
            right: number[];
            lookAt: number[];
            up: number[];
        };
    };
    title: string | undefined;
    subtitle: string | undefined;
};
export declare const ResolutionWidget: ({ obj, listLayers, viewId, camera, title, subtitle }: ResolutionWidgetProps) => JSX.Element;
export {};
