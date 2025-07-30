import React from "react";
import './VisWidget.css';
type visWidProps = {
    genericScreenPlotToggle: React.Dispatch<React.SetStateAction<any>>;
    modifyLabelPlot: any;
    listPlots: {
        id: number;
        hidden: boolean;
        svgId: string;
        label: string;
        checked: boolean;
        edit: boolean;
    }[];
};
export declare const VisWidget: ({ genericScreenPlotToggle, modifyLabelPlot, listPlots }: visWidProps) => JSX.Element;
export {};
