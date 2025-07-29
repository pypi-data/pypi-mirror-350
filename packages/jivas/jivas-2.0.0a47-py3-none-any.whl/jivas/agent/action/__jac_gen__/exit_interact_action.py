from __future__ import annotations
from jaclang import *
import typing
if typing.TYPE_CHECKING:
    from jivas.agent.core.graph_node import GraphNode
else:
    GraphNode, = jac_import('jivas.agent.core.graph_node', items={'GraphNode': None})
if typing.TYPE_CHECKING:
    from interact_action import InteractAction
else:
    InteractAction, = jac_import('interact_action', items={'InteractAction': None})
if typing.TYPE_CHECKING:
    from interact_graph_walker import interact_graph_walker
else:
    interact_graph_walker, = jac_import('interact_graph_walker', items={'interact_graph_walker': None})

class ExitInteractAction(InteractAction, Node):
    label: str = field('ExitInteractAction')
    description: str = field('core exit action node for walker cleanup and return')
    weight: int = field(10000)

    def touch(self, visitor: interact_graph_walker) -> bool:
        return True

    def execute(self, visitor: interact_graph_walker) -> dict:
        return {}