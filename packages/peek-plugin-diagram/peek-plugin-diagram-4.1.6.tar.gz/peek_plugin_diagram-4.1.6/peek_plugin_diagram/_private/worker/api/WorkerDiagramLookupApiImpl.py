from typing import List


from peek_plugin_base.worker import CeleryDbConn
from peek_plugin_diagram._private.storage.Lookups import DispColorTable
from peek_plugin_diagram._private.storage.Lookups import DispLayerTable
from peek_plugin_diagram._private.storage.Lookups import DispLevelTable
from peek_plugin_diagram._private.storage.Lookups import DispLineStyleTable
from peek_plugin_diagram._private.storage.Lookups import DispTextStyleTable
from peek_plugin_diagram.tuples.lookup_tuples.ShapeLayerTuple import (
    ShapeLayerTuple,
)


class WorkerDiagramLookupApiImpl:
    def __init__(self):
        pass

    @classmethod
    def getColors(cls) -> List[DispColorTable]:
        ormSession = CeleryDbConn.getDbSession()
        try:
            rows = ormSession.query(DispColorTable).all()

            tuples = []

            for row in rows:
                tuple_ = row.toTuple()
                tuples.append(tuple_)

            return tuples

        finally:
            ormSession.close()

    @classmethod
    def getLineStyles(cls) -> List[DispLineStyleTable]:
        ormSession = CeleryDbConn.getDbSession()
        try:
            rows = ormSession.query(DispLineStyleTable).all()

            tuples = []
            for row in rows:
                tuple_ = row.toTuple()
                tuples.append(tuple_)

            return tuples

        finally:
            ormSession.close()

    @classmethod
    def getTextStyles(cls) -> List[DispTextStyleTable]:
        ormSession = CeleryDbConn.getDbSession()
        try:
            rows = ormSession.query(DispTextStyleTable).all()

            tuples = []
            for row in rows:
                tuple_ = row.toTuple()
                tuples.append(tuple_)

            return tuples

        finally:
            ormSession.close()

    @classmethod
    def getLayers(cls) -> List[ShapeLayerTuple]:
        ormSession = CeleryDbConn.getDbSession()
        try:
            rows = ormSession.query(DispLayerTable).all()

            tuples = []
            for row in rows:
                tuple_ = row.toTuple()
                tuples.append(tuple_)

            return tuples

        finally:
            ormSession.close()

    @classmethod
    def getLevels(cls) -> List[DispLevelTable]:
        ormSession = CeleryDbConn.getDbSession()
        try:
            rows = ormSession.query(DispLevelTable).all()

            tuples = []
            for row in rows:
                tuple_ = row.toTuple()
                tuples.append(tuple_)

            return tuples

        finally:
            ormSession.close()
