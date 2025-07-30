/**
 * Multiply matrices of any dimensions given compatible columns and rows.
 */
export declare function multiplyMatrices(A: number[][], B: number[][]): number[][];
export declare function rotateYMatrix(a: number): number[][];
export declare function rotateZMatrix(a: number): number[][];
export declare function translateMatrix(x: number, y: number, z: number): number[][];
export declare function dot(v1: number[], v2: number[]): number;
export declare function angle(v1: number[], v2: number[]): number;
export declare function radians(angle: number): number;
export declare function degree(radians: number): number;
export declare function cross(a: any[], b: any[]): number[];
export declare function normalize(a: number[]): number[];
export declare function add(a: any[], b: any[]): any[];
export declare function sub(a: number[], b: number[]): number[];
export declare function euclideanDistance(p1: number[], p2: number[]): number;
