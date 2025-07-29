from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})

class delete_agent(agent_graph_walker, Walker):
    agent_id: str = field('')

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agents(self, here: Agents) -> None:
        agent_node = here.delete(self.agent_id)
        if self.reporting:
            Jac.report(agent_node)