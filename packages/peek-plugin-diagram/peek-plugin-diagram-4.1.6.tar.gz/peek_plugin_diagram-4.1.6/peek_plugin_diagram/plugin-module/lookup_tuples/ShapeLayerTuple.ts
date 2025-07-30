import { addTupleType, Tuple } from "@synerty/vortexjs";
import { diagramTuplePrefix } from "@peek/peek_plugin_diagram/_private";

@addTupleType
export class ShapeLayerTuple extends Tuple {
    public static readonly tupleName = diagramTuplePrefix + "ShapeLayerTuple";

    key: string;
    modelSetKey: string;
    name: string;
    order: number;
    selectable: boolean;
    visible: boolean;
    opacity: number;
    showForEdit: boolean;

    constructor() {
        super(ShapeLayerTuple.tupleName);
    }
}
