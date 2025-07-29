from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from graph_node import GraphNode
else:
    GraphNode, = jac_import('graph_node', items={'GraphNode': None})
if typing.TYPE_CHECKING:
    from purge import purge
else:
    purge, = jac_import('purge', items={'purge': None})

class Agents(GraphNode, Node):
    logger: static[Logger] = logging.getLogger(__name__)

    def get_all(self) -> list:
        return self.refs()

    def get_by_name(self, name: str) -> None:
        return Utils.node_obj(self.refs().filter(None, lambda item: item.name == name))

    def get_by_id(self, id: str) -> None:
        return Utils.node_obj(self.refs().filter(None, lambda item: item.id == id))

    def delete(self, id: str) -> None:
        if (agent_node := self.get_by_id(id)):
            agent_node.get_actions().deregister_actions()
            agent_node.spawn(purge())
            return agent_node
        return None

    def delete_all(self) -> None:
        agent_nodes = JacList([])
        for agent_node in self.get_all():
            agent_nodes.append(self.delete(agent_node.id))
        return agent_nodes