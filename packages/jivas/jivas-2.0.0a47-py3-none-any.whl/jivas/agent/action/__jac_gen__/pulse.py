from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from action import Action
else:
    Action, = jac_import('action', items={'Action': None})
if typing.TYPE_CHECKING:
    from jivas.agent.action.actions import Actions
else:
    Actions, = jac_import('jivas.agent.action.actions', items={'Actions': None})
if typing.TYPE_CHECKING:
    from interact_graph_walker import interact_graph_walker
else:
    interact_graph_walker, = jac_import('interact_graph_walker', items={'interact_graph_walker': None})

class pulse(interact_graph_walker, Walker):
    action_label: str = field('')
    agent_id: str = field('')

    class __specs__(Obj):
        auth: static[bool] = True

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        self.visit(here.refs().filter(Action, None).filter(None, lambda item: item.enabled == True).filter(None, lambda item: item.label == self.action_label))

    @with_entry
    def on_action(self, here: Action) -> None:
        here.pulse()