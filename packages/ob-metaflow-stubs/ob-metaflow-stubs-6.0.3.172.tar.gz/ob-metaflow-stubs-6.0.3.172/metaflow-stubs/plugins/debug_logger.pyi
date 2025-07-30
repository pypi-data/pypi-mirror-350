######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.14.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-27T03:43:23.555303                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger


class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

