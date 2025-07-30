import { addTupleType, Tuple } from "@synerty/vortexjs";
import { diagramTuplePrefix } from "@peek/peek_plugin_diagram/_private";
import { ShapeLayerTuple } from "@peek/peek_plugin_diagram/lookup_tuples";

@addTupleType
export class DispLayer extends Tuple {
    public static readonly tupleName = diagramTuplePrefix + "DispLayer";

    // Tuple Fields
    key: string;
    modelSetKey: string;

    id: number;
    name: string;

    importHash: string;
    showForEdit: boolean;
    blockApiUpdate: boolean;

    order: number;
    selectable: boolean;
    visible: boolean;
    opacity: number;
    modelSetId: number;

    constructor() {
        super(DispLayer.tupleName);
    }

    toTuple(): ShapeLayerTuple {
        const tuple_ = new ShapeLayerTuple();
        tuple_.key = this.key;
        tuple_.modelSetKey = this.modelSetKey;

        tuple_.name = this.name;
        tuple_.showForEdit = this.showForEdit;

        tuple_.order = this.order;
        tuple_.selectable = this.selectable;
        tuple_.visible = this.visible;
        tuple_.opacity = this.opacity;

        return tuple_;
    }
}
