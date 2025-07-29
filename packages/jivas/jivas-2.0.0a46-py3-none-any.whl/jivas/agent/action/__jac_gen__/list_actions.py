from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import yaml
else:
    yaml, = jac_import('yaml', 'py')
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
if typing.TYPE_CHECKING:
    from interact_action import InteractAction
else:
    InteractAction, = jac_import('interact_action', items={'InteractAction': None})

class list_actions(interact_graph_walker, Walker):
    agent_id: str = field('')
    actions: list = field(gen=lambda: JacList([]))
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False
        excluded: static[list] = JacList(['actions'])

    @with_entry
    def on_agent(self, here: Agent) -> None:
        self.visit(here.refs().filter(Actions, None))

    @with_entry
    def on_actions(self, here: Actions) -> None:
        self.visit(here.refs().filter(Action, None))

    @with_entry
    def on_action(self, here: Action) -> None:
        action_data = here.export()
        self.actions.append(action_data)
        self.visit(here.refs().filter(Action, None))

    @with_exit
    def on_exit(self, here) -> None:
        other_actions = JacList([action for action in self.actions if action.get('_package', {}).get('meta', {}).get('type', 'action') != 'interact_action' and action['label'] != 'ExitInteractAction'])
        interact_actions = JacList([action for action in self.actions if action.get('_package', {}).get('meta', {}).get('type', 'action') == 'interact_action' or action['label'] == 'ExitInteractAction'])
        self.actions = sorted(interact_actions, key=lambda action: int: action['weight']) + other_actions
        Jac.report(self.actions)