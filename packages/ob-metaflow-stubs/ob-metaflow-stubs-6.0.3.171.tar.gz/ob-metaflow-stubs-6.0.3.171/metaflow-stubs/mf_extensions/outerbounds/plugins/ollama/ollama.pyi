######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.14.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-27T00:40:42.119055                                                            #
######################################################################################################

from __future__ import annotations


from .exceptions import EmptyOllamaManifestCacheException as EmptyOllamaManifestCacheException
from .exceptions import EmptyOllamaBlobCacheException as EmptyOllamaBlobCacheException
from .exceptions import UnspecifiedRemoteStorageRootException as UnspecifiedRemoteStorageRootException

OLLAMA_SUFFIX: str

class ProcessStatus(object, metaclass=type):
    ...

class OllamaManager(object, metaclass=type):
    """
    A process manager for Ollama runtimes.
    Implements interface @ollama([models=...], ...) has a local, remote, or managed backend.
    """
    def __init__(self, models, backend = 'local', flow_datastore_backend = None, remote_storage_root = None, force_pull = False, skip_push_check = False, debug = False):
        ...
    def terminate_models(self, skip_push_check = None):
        """
        Terminate all processes gracefully and update cache.
        """
        ...
    def get_ollama_storage_root(self, backend):
        """
        Return the path to the root of the datastore.
        """
        ...
    ...

