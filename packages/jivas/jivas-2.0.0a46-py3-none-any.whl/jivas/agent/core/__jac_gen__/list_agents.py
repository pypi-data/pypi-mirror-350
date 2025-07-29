from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from app import App
else:
    App, = jac_import('app', items={'App': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})

class list_agents(agent_graph_walker, Walker):

    class __specs__(Obj):
        private: static[bool] = False
        excluded: static[list] = JacList(['agent_id'])

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if (agents := here.get_all()):
            for agent in agents:
                Jac.report(agent.export())