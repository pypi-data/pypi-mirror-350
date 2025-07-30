from vortex.Tuple import Tuple, addTupleType, TupleField

from peek_plugin_diagram._private.PluginNames import diagramTuplePrefix


@addTupleType
class ImportDispLayerTuple(Tuple):
    """Import Display Layer Tuple"""

    __tupleType__ = diagramTuplePrefix + "ImportDispLayerTuple"

    name: str = TupleField()

    order: int = TupleField()

    selectable: bool = TupleField()

    visible: bool = TupleField()

    #: Opacity, Should shapes on this layer be rendered partially see though?
    # Range is 0.00 to 1.00
    opacity: float = TupleField(defaultValue=1.0)

    importHash: str = TupleField()

    modelSetKey: str = TupleField()

    showForEdit: bool = TupleField(defaultValue=False)

    blockApiUpdate: bool = TupleField(defaultValue=False)
