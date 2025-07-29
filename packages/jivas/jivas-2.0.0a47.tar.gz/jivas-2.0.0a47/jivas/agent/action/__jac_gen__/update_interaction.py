from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.interaction import Interaction
else:
    Interaction, = jac_import('jivas.agent.memory.interaction', items={'Interaction': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_walker import graph_walker
else:
    graph_walker, = jac_import('jivas.agent.core.graph_walker', items={'graph_walker': None})
if typing.TYPE_CHECKING:
    from jac_cloud.core.architype import NodeAnchor
else:
    NodeAnchor, = jac_import('jac_cloud.core.architype', 'py', items={'NodeAnchor': None})

class update_interaction(graph_walker, Walker):
    logger: static[Logger] = logging.getLogger(__name__)
    interaction_data: dict = field(gen=lambda: {})

    class __specs__(Obj):
        auth: static[bool] = True
        private: static[bool] = False

    @with_entry
    def on_interaction(self, here: Interaction) -> None:
        if not self.interaction_data:
            self.logger.error('no interaction data')
            return
        here.update(data=self.interaction_data)
        here.close()