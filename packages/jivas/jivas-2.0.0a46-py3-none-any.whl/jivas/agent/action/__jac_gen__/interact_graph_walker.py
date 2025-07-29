from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('jivas.agent.core.agent_graph_walker', items={'agent_graph_walker': None})

class interact_graph_walker(agent_graph_walker, Walker):
    pass