from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})

class get_agent(agent_graph_walker, Walker):

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        Jac.report(here.export())