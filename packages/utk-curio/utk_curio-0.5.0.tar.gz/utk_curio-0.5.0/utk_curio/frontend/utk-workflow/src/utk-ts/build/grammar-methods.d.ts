import { IMasterGrammar } from './interfaces';
export declare class GrammarMethods {
    static grammar: IMasterGrammar;
    static subscribers: any;
    static applyGrammar(url_string: string | undefined, grammar: Object, identifier: string, callback_function: Function, filename: string): Promise<any>;
    static subscribe(identifier: string, subscription_callback: Function): void;
    static updateGrammar(data: IMasterGrammar): void;
}
