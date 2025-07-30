import logging
from abc import ABCMeta
from typing import Optional
from typing import Union

from sqlalchemy.exc import NoResultFound
from twisted.internet.defer import Deferred
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.TupleSelector import TupleSelector
from vortex.data_loader.TupleDataLoaderDelegate import (
    TupleDataLoaderDelegateABC,
)
from vortex.data_loader.TupleDataLoaderTupleABC import TupleDataLoaderTupleABC

from peek_plugin_diagram._private.logic.tuple_change_event_bus.diagram_tuple_change_event_bus import (
    plDiagramTupleChangeEventBus,
)
from peek_plugin_diagram._private.logic.tuple_change_event_bus.lookup_color_config_change_event import (
    LookupColorConfigChangeEvent,
)
from peek_plugin_diagram._private.storage.Lookups import DispColorTable
from peek_plugin_diagram._private.tuples.admin.config_color_lookup_data_loader_tuple import (
    ConfigColorLookupDataLoaderTuple,
)


logger = logging.getLogger(__name__)


class ConfigLookupTupleDataLoaderDelegateBase(
    TupleDataLoaderDelegateABC, metaclass=ABCMeta
):
    TableOrmClass = None

    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    def _makeUniqueImportHash(self, item, ormSession):
        if not item.importHash:
            return

        if hasattr(item, "coordSetId"):
            filt = dict(coordSetId=item.coordSetId)
        else:
            filt = dict(modelSetId=item.modelSetId)

        copyNum = 2
        originalImportHash = item.importHash
        while (
            ormSession.query(self.TableOrmClass)
            .filter_by(importHash=item.importHash, **filt)
            .one_or_none()
        ):
            item.importHash = f"{originalImportHash}-{copyNum}"
            copyNum = copyNum + 1

    @deferToThreadWrapWithLogger(logger)
    def deleteData(self, tupleSelector: TupleSelector) -> Deferred:
        raise NotImplementedError("We don't delete settings")
