export declare class InteractionChannel {
    static getGrammar: Function;
    static modifyGrammar: Function;
    static modifyGrammarVisibility: Function;
    static passedVariables: {
        [key: string]: any;
    };
    static setModifyGrammarVisibility(modifyGrammar: Function): void;
    static getModifyGrammarVisibility(): Function;
    static addToPassedVariables(name: string, value: any): void;
    static getPassedVariable(name: string): any;
    static sendData(variable: {
        name: string;
        value: any;
    }): void;
}
