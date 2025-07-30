######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.14.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-05-27T00:40:42.093609                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector
    import metaflow.decorators

from ...metaflow_current import current as current
from ...mf_extensions.outerbounds.plugins.ollama import constants as constants
from ...mf_extensions.outerbounds.plugins.ollama import exceptions as exceptions
from ...mf_extensions.outerbounds.plugins.ollama import ollama as ollama
from ...mf_extensions.outerbounds.plugins.ollama.ollama import OllamaManager as OllamaManager
from ...mf_extensions.outerbounds.plugins.card_utilities.injector import CardDecoratorInjector as CardDecoratorInjector

class OllamaDecorator(metaflow.decorators.StepDecorator, metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector.CardDecoratorInjector, metaclass=type):
    """
    This decorator is used to run Ollama APIs as Metaflow task sidecars.
    
    User code call
    --------------
    @ollama(
        models=[...],
        ...
    )
    
    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.
    - (TODO) 'managed': Outerbounds hosts and selects compute provider.
    - (TODO) 'remote': Spin up separate instance to serve Ollama models.
    
    Valid model options
    -------------------
    Any model here https://ollama.com/search, e.g. 'llama3.2', 'llama3.3'
    
    Parameters
    ----------
    models: list[str]
        List of Ollama containers running models in sidecars.
    backend: str
        Determines where and how to run the Ollama process.
    force_pull: bool
        Whether to run `ollama pull` no matter what, or first check the remote cache in Metaflow datastore for this model key.
    skip_push_check: bool
        Whether to skip the check that populates/overwrites remote cache on terminating an ollama model.
    debug: bool
        Whether to turn on verbose debugging logs.
    """
    def step_init(self, flow, graph, step_name, decorators, environment, flow_datastore, logger):
        ...
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

