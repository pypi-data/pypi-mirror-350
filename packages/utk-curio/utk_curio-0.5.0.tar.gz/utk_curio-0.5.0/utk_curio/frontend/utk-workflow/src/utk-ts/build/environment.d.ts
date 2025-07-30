export declare class Environment {
    static backend: string;
    static serverless: boolean;
    /**
     * Set environment parameters
     * @param {{backend: string}} env Environment parameters
     */
    static setEnvironment(env: {
        backend: string;
    }): void;
}
