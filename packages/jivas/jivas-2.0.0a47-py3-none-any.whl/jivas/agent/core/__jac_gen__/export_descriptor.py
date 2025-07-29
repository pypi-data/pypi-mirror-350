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
if typing.TYPE_CHECKING:
    from jivas.agent.action.action import Action
else:
    Action, = jac_import('jivas.agent.action.action', items={'Action': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})

class export_descriptor(agent_graph_walker, Walker):
    as_yaml: bool = field(False)
    clean: bool = field(False)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        Jac.report(here.get_descriptor(as_yaml=self.as_yaml, clean=self.clean))