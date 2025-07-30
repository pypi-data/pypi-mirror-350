import logging

from peek_plugin_base.worker.PluginWorkerEntryHookABC import (
    PluginWorkerEntryHookABC,
)
from peek_plugin_diagram._private.worker.tasks import (
    GridCompilerTask,
    ImportDispTask,
    DispCompilerTask,
    LocationIndexCompilerTask,
)
from peek_plugin_diagram._private.worker.tasks.branch import (
    BranchIndexCompilerTask,
    BranchIndexImporterTask,
    BranchIndexUpdaterTask,
)
from peek_plugin_diagram.tuples import loadPublicTuples

logger = logging.getLogger(__name__)


class WorkerEntryHook(PluginWorkerEntryHookABC):
    def load(self):
        loadPublicTuples()
        logger.debug("loaded")

    def start(self):
        logger.debug("started")

    def stop(self):
        logger.debug("stopped")

    def unload(self):
        logger.debug("unloaded")

    @property
    def celeryAppIncludes(self):
        return [
            BranchIndexUpdaterTask.__name__,
            BranchIndexCompilerTask.__name__,
            BranchIndexImporterTask.__name__,
            DispCompilerTask.__name__,
            GridCompilerTask.__name__,
            ImportDispTask.__name__,
            LocationIndexCompilerTask.__name__,
        ]
