import { DispBasePartial, DispBaseT } from "../canvas-shapes/DispBasePartial";

/** Sort Disps
 *
 * This method sorts disps in the order needed for the model to compile them for the
 * renderer.
 *
 * This method was initially written for the BranchTuple.
 *
 * WARNING: Sorting disps is terrible for performance, this is only used while
 * the branch is being edited by the user.
 *
 * @param disps: A List of disps to sort
 * @returns: A list of sorted disps
 */
export function sortDisps(disps: DispBaseT[]): DispBaseT[] {
    function cmp(d1: DispBaseT, d2: DispBaseT): number {
        let levelDiff =
            DispBasePartial.level(d1).order - DispBasePartial.level(d2).order;
        if (levelDiff != 0) return levelDiff;

        let layerDiff =
            DispBasePartial.layer(d1).order - DispBasePartial.layer(d2).order;
        if (layerDiff != 0) return layerDiff;

        return DispBasePartial.zOrder(d1) - DispBasePartial.zOrder(d2);
    }

    return disps.sort(cmp);
}
