export declare abstract class GeoUtils {
    static res: number;
    static wLevel: number;
    /**
     * Converts from lat, lng to world coordinates
     * @param {number} latitude the latitude of the point
     * @param {number} longitude the longitude of the point
     */
    static latLng2Coord_old(latitude: number, longitude: number): number[];
    static latLng2Coord(latitude: number, longitude: number): number[];
    /**
     * Converts from world coordinates to lat, lng
     * @param {number} x the x coordinate of the point
     * @param {number} y the y coordinate of the point
     */
    static coord2LatLng_old(x: number, y: number): number[];
    static coord2LatLng(x: number, y: number): number[];
    /**
     * Computes the ground resolution
     * @param {number} lat the latitude value
     * @param {number} lng the longitude value
     * @param {number} zoom the zoom leevl
     */
    static groundResolution(lat: number, lng: number, zoom: number): number;
    static latlonToWebMercator(lat: number, lon: number): number[];
}
