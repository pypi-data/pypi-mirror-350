export declare abstract class DataLoader {
    /**
     * Loads a json file
     * @param {string} url json file url
     * @returns {Promise<unknown>} The load json promise
     */
    static getJsonData(url: string): Promise<unknown>;
    static getBinaryData(url: string, type: string): Promise<unknown>;
    /**
     * Loads a text file
     * @param {string} url text file url
     * @returns {Promise<string>} The load text promise
     */
    static getTextData(url: string): Promise<string>;
}
